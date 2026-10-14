from typing import Annotated

from fastapi import Depends, FastAPI

from app.auth import get_current_user
from app.models import User

app = FastAPI(title="Job Tracker API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/me")
def read_me(user: Annotated[User, Depends(get_current_user)]) -> dict[str, str]:
    return {"id": str(user.id), "cognito_sub": user.cognito_sub}
