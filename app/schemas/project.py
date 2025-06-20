from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ProjectType(str, Enum):
    single_family_home = "single_family_home"
    residential_building = "residential_building"
    commercial_building = "commercial_building"
    industrial = "industrial"
    renovation = "renovation"
    recreational = "recreational"
    other = "other"
    
class Currency(str, Enum):
    ars = "ars"
    usd = "usd"
    eur = "eur"

class ProjectStatus(str, Enum):
    idea = "idea"
    budgeting = "budgeting"
    in_progress = "in_progress"
    finished = "finished"

class FileType(str, Enum):
    bim_model = "bim_model"
    blueprints = "blueprints"
    renders = "renders"
    material_takeoff = "material_takeoff"

class ProjectBase(BaseModel):
    name: str
    client_id: int
    project_type: ProjectType
    currency: Currency
    budget: float
    location: str
    status: ProjectStatus

    class Config:
        use_enum_values = True

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str]
    project_type: Optional[ProjectType]
    currency: Optional[Currency]
    budget: Optional[float]
    location: Optional[str]
    status: Optional[ProjectStatus]

class ProjectInDB(ProjectBase):
    id: int
    created_at: Optional[datetime] = Field(None, alias="create_date")
    updated_at: Optional[datetime] = Field(None, alias="update_date")

    class Config:
        fro_attribute= True
        validate_by_name = True
