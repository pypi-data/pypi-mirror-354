import json
import os
from dataclasses import field
from typing import Optional

from flexrag.utils import configure, data
from flexrag.utils.dataclasses import Context

from .dataset import MappingDataset


@configure
class MTEBDatasetConfig:
    """Configuration for loading `MTEB <https://huggingface.co/mteb>`_ Retrieval Dataset.
    The __getitem__ method will return `IREvalData` objects.

    For example, to load the NQ dataset, you can download the test set by running the following command:

        >>> git lfs install
        >>> git clone https://huggingface.co/datasets/mteb/nq nq

    Then you can use the following code to load the dataset:

        >>> config = MTEBDatasetConfig(
        ...     data_path="nq",
        ...     subset="test",
        ...     load_corpus=False,
        ... )
        >>> dataset = MTEBDataset(config)

    :param data_path: Path to the data directory. Required.
    :type data_path: str
    :param subset: Subset of the dataset to load. Required.
    :type subset: str
    :param encoding: Encoding of the data files. Default is 'utf-8'.
    :type encoding: str
    :param load_corpus: Whether to load the corpus data. Default is False.
    :type load_corpus: bool
    """

    data_path: str
    subset: str
    encoding: str = "utf-8"
    load_corpus: bool = False


@data
class IREvalData:
    """The dataclass for Information Retrieval evaluation data.

    :param question: The question for evaluation. Required.
    :type question: str
    :param contexts: The contexts related to the question. Default: None.
    :type contexts: Optional[list[Context]]
    :param meta_data: The metadata of the evaluation data. Default: {}.
    :type meta_data: dict
    """

    question: str
    contexts: Optional[list[Context]] = None
    meta_data: dict = field(default_factory=dict)


class MTEBDataset(MappingDataset[IREvalData]):
    """Dataset for loading MTEB Retrieval Dataset."""

    def __init__(self, config: MTEBDatasetConfig) -> None:
        qrels: list[dict] = [
            json.loads(line)
            for line in open(
                os.path.join(config.data_path, "qrels", f"{config.subset}.jsonl"),
                "r",
                encoding=config.encoding,
            )
        ]
        queries = [
            json.loads(line)
            for line in open(
                os.path.join(config.data_path, "queries.jsonl"),
                "r",
                encoding=config.encoding,
            )
        ]
        queries = {query["_id"]: query for query in queries}

        if config.load_corpus:
            corpus = [
                json.loads(line)
                for line in open(
                    os.path.join(config.data_path, "corpus.jsonl"),
                    "r",
                    encoding=config.encoding,
                )
            ]
            corpus = {doc["_id"]: doc for doc in corpus}
        else:
            corpus = None

        # merge qrels, queries, and corpus into RetrievalData
        dataset_map: dict[str, int] = {}
        self.dataset: list[IREvalData] = []
        for qrel in qrels:
            # construct the context
            context = Context(context_id=qrel["corpus-id"])
            if corpus is not None:
                context.data = corpus[qrel["corpus-id"]]
            if "score" in qrel:  # relevance level of the context
                context.meta_data["score"] = int(qrel["score"])
            query = queries[qrel["query-id"]]["text"]

            if qrel["query-id"] not in dataset_map:
                dataset_map[qrel["query-id"]] = len(self.dataset)
                self.dataset.append(
                    IREvalData(
                        question=query,
                        contexts=[context],
                        meta_data={"query-id": qrel["query-id"]},
                    )
                )
            else:
                index = dataset_map[qrel["query-id"]]
                self.dataset[index].contexts.append(context)
        return

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, index: int) -> IREvalData:
        return self.dataset[index]
