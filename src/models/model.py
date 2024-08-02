from abc import ABC, abstractmethod


class Model(ABC):

    @property
    @abstractmethod
    def url(self):
        pass

    @property
    @abstractmethod
    def input_token_cost(self):
        pass

    @property
    @abstractmethod
    def output_token_cost(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    async def label(self):
        pass

    @abstractmethod
    async def get_token_cost(self):
        pass
