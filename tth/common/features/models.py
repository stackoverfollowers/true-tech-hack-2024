from pydantic import BaseModel, ConfigDict


class FeatureModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
