from __future__ import annotations
from otex.utils.http_utils import Call, Response 
from abc import ABC, abstractmethod
from typing import List

class AbstractLiquidityPoolPrimitive(ABC):
    chain_id: int
    protocol_id: str
    pool_address: str
    tokens: list[str]
    computation_units: dict
    protocol_utils: dict

    @abstractmethod
    def to_dict(
        self,
        deep: bool = False
    ) -> dict:
        pass

    @abstractmethod
    def get_pool_states_calls(
        self
    ) -> List[Call]:
        pass

    @abstractmethod
    def get_pool_dependent_states_calls(
        self
    ) -> List[Call]:
        pass

    @abstractmethod
    def process_pool_state_call_response(
        self,
        data: Response
    ) -> None:
        pass

    @abstractmethod
    def has_complete_pool_states(
        self
    ) -> bool:
        pass

    @abstractmethod
    def get_amount_out(
        self, 
        token_in: str, 
        amount_in: int,
        token_out: str = None
    ) -> tuple[int | None , int | None]:
        pass

    @abstractmethod
    def get_amount_in(
        self, 
        token_out: str, 
        amount_in: int,
        token_in: str = None
    ) -> tuple[int | None, int | None]:
        pass

    @abstractmethod
    def get_interaction_encoding_utils(
        self, 
        token_in:str, 
        amount_in:int, 
        token_out:str, 
        amount_out:int
    ) -> dict:
        pass
