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