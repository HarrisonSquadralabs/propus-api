from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models import Project, User, UserRole
from app.schemas.project import ProjectCreate, ProjectInDB, ProjectUpdate
from app.core.deps import require_role, get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

# Only architects can access
architect_required = Depends(require_role(UserRole.architect))

@router.post("/", response_model=ProjectInDB, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = architect_required,
):
    project_data = project.dict(exclude_unset=True)
    project_data["architect_id"] = current_user.id

    db_project = Project(**project_data)

    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)

    return db_project

@router.get("/", response_model=List[ProjectInDB])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.architect)),
):
    result = await db.execute(
        select(Project).where(Project.architect_id == current_user.id)
    )
    projects = result.scalars().all()
    return projects

@router.patch("/{project_id}", response_model=ProjectInDB)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.architect)),
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if project.architect_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this project")

    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)

    return project