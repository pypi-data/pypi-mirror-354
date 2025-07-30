from pydantic import BaseModel


class TransientCase(BaseModel):
    L_0: int
    λ: float
    μ: float
    ls_max: int
    time_step: float
