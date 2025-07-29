from typing import Dict, Generic, Iterable, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")


class ElementBindingMixin(ABC, Generic[T]):
    @abstractmethod
    def _to_element_binding_config(self) -> Dict:
        pass

    def _mark_used(self):
        pass

    def _is_used(self):
        return True


def _try_mark_inputs_used(inputs: Iterable):
    for input_ in inputs:
        if isinstance(input_, ElementBindingMixin):
            input_._mark_used()
