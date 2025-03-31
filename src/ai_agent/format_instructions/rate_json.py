from pydantic import BaseModel, Field


class RateJSON(BaseModel):
    rate: int = Field(description="Дай оценку от 1 до 10, где 10 идеально составленное задание, а 1 плохо составленное задание сотруднику")
