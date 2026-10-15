import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import Application, User
from app.schemas.application import ApplicationCreate, ApplicationRead

router = APIRouter(prefix="/applications", tags=["applications"])

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(body: ApplicationCreate, db: DbSession, user: CurrentUser) -> Application:
    application = Application(**body.model_dump(), user_id=user.id)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("", response_model=list[ApplicationRead])
def list_applications(db: DbSession, user: CurrentUser) -> list[Application]:
    stmt = (
        select(Application)
        .where(Application.user_id == user.id)
        .order_by(Application.last_activity_at.desc())
    )
    return list(db.scalars(stmt).all())


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: uuid.UUID, db: DbSession, user: CurrentUser) -> Application:
    stmt = select(Application).where(
        Application.id == application_id, Application.user_id == user.id
    )
    application = db.scalars(stmt).first()
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application
