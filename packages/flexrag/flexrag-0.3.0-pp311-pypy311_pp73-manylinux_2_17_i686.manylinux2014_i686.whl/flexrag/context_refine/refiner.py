from abc import ABC, abstractmethod

from flexrag.utils import Register
from flexrag.utils.dataclasses import RetrievedContext


class RefinerBase(ABC):
    """The base class for context refiners.
    The subclasses should implement the ``refine`` method.
    """

    @abstractmethod
    def refine(self, contexts: list[RetrievedContext]) -> list[RetrievedContext]:
        """Refine the contexts.

        :param contexts: The retrieved contexts to refine.
        :type contexts: list[RetrievedContext]
        :return: The refined contexts.
        :rtype: list[RetrievedContext]
        """
        return


REFINERS = Register[RefinerBase]("refiner")
