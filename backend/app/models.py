from pydantic import BaseModel

class RiskEntity(BaseModel):
    entity_id: str
    total_score: float
    risk_level: str

class PostExplainability(BaseModel):
    post_id: str
    indicator_type: str
    indicator_value: str
    weight: float
