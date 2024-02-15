from typing import Literal, Any
from dataclasses import dataclass

@dataclass
class Call:
    url: str # URL to which HTTP call will be made
    http_method: Literal["POST", "GET"] 
    request_type: Literal['quote', 'solve', 'state']
    chain_id: str # Blockchain context for which we execute the call
    protocol_id: str # Protoocl context for which we need the  call
    body: dict # body of HTTP request
    attribute: str # identifier for state calls
    detail: dict # further information needed to process the Call later on

    def add_call_id(
        self,
        suffix:str
    ) -> None:
        if suffix:
            self.call_id = self.chain_id + '_' + self.protocol_id + '_' + self.request_type + '_' + suffix
        else:
            self.call_id = self.chain_id + '_' + self.protocol_id + '_' + self.request_type
    
    def add_body(
        self,
        body: dict()
    ) -> None:
        self.body = body
    
    def add_headers(
        self,
        headers: dict()
    ) -> None:
        self.headers = headers


@dataclass
class Response:
    result: Any
    attribute: str
    detail: dict
