from dataclasses import dataclass
from typing import List
import json

@dataclass
class BusinessRecord:
    region : str
    product : str
    sales : int
    reveneu : float

@dataclass
class AgentState:
    data: List[BusinessRecord] 
    question:str
    recommendation : str

    @staticmethod
    def from_json(json_str : str) -> AgentState: # type: ignore
        raw = json.loads(json_str)
        records = [BusinessRecord(**rec) for rec in raw['data']]
        return AgentState(data=records, question=raw['question'])