from abc import ABC, abstractmethod


class Model(ABC):

    @abstractmethod
    @property
    def endpoint(self):
        pass

    @abstractmethod
    @property
    def input_token_cost(self):
        pass

    @abstractmethod
    @property
    def output_token_cost(self):
        pass

    @abstractmethod
    async def label(self):
        pass

    @abstractmethod
    async def get_token_cost(self):
        pass
