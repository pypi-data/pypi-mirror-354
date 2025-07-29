from abc import ABC, abstractmethod
from dataclasses import field

from flexrag.utils import Register, data


@data
class TextUnit:
    content: str
    reserved: bool = True
    processed_by: list[str] = field(default_factory=list)


class Processor(ABC):
    def __call__(self, input_text: TextUnit | str) -> TextUnit | str:
        """Process the input text.
        If the processor has been filtered, the reserved flag of the input TextUnit will be set to False.

        :param input_text: The input text to process.
        :type input_text: TextUnit
        :return: The processed text.
        :rtype: TextUnit
        """
        if isinstance(input_text, str):
            input_text = TextUnit(content=input_text)
            return self.process(input_text).content
        input_text.processed_by.append(self.name)
        return self.process(input_text)

    @abstractmethod
    def process(self, input_text: TextUnit) -> TextUnit:
        return

    @property
    def name(self):
        return self.__class__.__name__


PROCESSORS = Register[Processor]("processor")
