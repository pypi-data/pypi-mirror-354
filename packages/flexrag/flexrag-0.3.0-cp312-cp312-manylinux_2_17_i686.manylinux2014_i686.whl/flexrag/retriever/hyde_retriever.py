from typing import Annotated

from flexrag.models import GENERATORS, GeneratorBase, GeneratorConfig
from flexrag.utils import TIME_METER, Choices, configure
from flexrag.utils.dataclasses import RetrievedContext

from .flex_retriever import FlexRetriever, FlexRetrieverConfig
from .retriever_base import RETRIEVERS


class HydeRewriter:
    Prompts = {
        "WEB_SEARCH": "Please write a passage to answer the question.\nQuestion: {}\nPassage:",
        "SCIFACT": "Please write a scientific paper passage to support/refute the claim.\nClaim: {}\nPassage:",
        "ARGUANA": "Please write a counter argument for the passage.\nPassage: {}\nCounter Argument:",
        "TREC_COVID": "Please write a scientific paper passage to answer the question.\nQuestion: {}\nPassage:",
        "FIQA": "Please write a financial article passage to answer the question.\nQuestion: {}\nPassage:",
        "DBPEDIA_ENTITY": "Please write a passage to answer the question.\nQuestion: {}\nPassage:",
        "TREC_NEWS": "Please write a news passage about the topic.\nTopic: {}\nPassage:",
        "MR_TYDI": "Please write a passage in {} to answer the question in detail.\nQuestion: {}\nPassage:",
    }

    def __init__(self, generator: GeneratorBase, task: str, language: str = "en"):
        self.task = task
        self.language = language
        self.generator = generator
        return

    @TIME_METER("hyde_retriever", "rewrite")
    def rewrite(self, queries: list[str] | str) -> list[str]:
        if isinstance(queries, str):
            queries = [queries]
        prompts = [self.Prompts[self.task].format(q) for q in queries]
        new_queries = [q[0] for q in self.generator.generate(prompts)]
        return new_queries


@configure
class HydeRetrieverConfig(FlexRetrieverConfig, GeneratorConfig):
    """Configuration class for HydeRetriever.

    :param task: Task for rewriting the query. Default: "WEB_SEARCH".
        Available options: "WEB_SEARCH", "SCIFACT", "ARGUANA", "TREC_COVID", "FIQA", "DBPEDIA_ENTITY", "TREC_NEWS", "MR_TYDI".
    :type task: str
    :param language: Language for rewriting. Default: "en".
    :type language: str
    """

    task: Annotated[str, Choices(*HydeRewriter.Prompts.keys())] = "WEB_SEARCH"
    language: str = "en"


@RETRIEVERS("hyde", config_class=HydeRetrieverConfig)
class HydeRetriever(FlexRetriever):
    """HydeRetriever is a retriever that rewrites the query before searching.

    The original paper is available at https://aclanthology.org/2023.acl-long.99/.
    """

    def __init__(self, cfg: HydeRetrieverConfig, no_check=False):
        super().__init__(cfg, no_check)
        generator = GENERATORS.load(cfg)
        self.rewriter = HydeRewriter(
            generator=generator, task=cfg.task, language=cfg.language
        )
        return

    def search(
        self,
        query: list[str],
        **search_kwargs,
    ) -> list[list[RetrievedContext]]:
        new_query = self.rewriter.rewrite(query)
        return super().search(new_query, **search_kwargs)
