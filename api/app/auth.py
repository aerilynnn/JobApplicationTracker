from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import User

# Reads the "Authorization: Bearer <token>" header and adds an Authorize button to /docs.
bearer_scheme = HTTPBearer()

# Downloads Cognito's public keys the first time it needs them, then caches them.
jwks_client = jwt.PyJWKClient(settings.cognito_jwks_url)


def verify_token(token: str) -> dict[str, Any]:
    """Check a Cognito access token and return its claims.

    Raises HTTPException(401) if the token is invalid for any reason.
    """
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        decoded_token = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            issuer=settings.cognito_issuer,
            options={"require": ["exp", "iss", "sub", "token_use", "client_id"]},
        )

        if decoded_token["token_use"] != "access":
            raise jwt.InvalidTokenError("Token is not an access token")

        if decoded_token["client_id"] != settings.cognito_client_id:
            raise jwt.InvalidTokenError("Token was not issued for this app")

    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    return decoded_token


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Return the logged-in user, creating their row on first sight."""
    decoded_token = verify_token(credentials.credentials)
    cognito_sub = decoded_token["sub"]

    stmt = select(User).where(User.cognito_sub == cognito_sub)
    user = db.scalar(stmt)

    # First request from this user: create their row (just-in-time provisioning).
    if user is None:
        try:
            user = User(cognito_sub=cognito_sub)
            db.add(user)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            # Another request created this user at the same moment; use their row.
            db.rollback()
            user = db.scalar(stmt)

    return user
