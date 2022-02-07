from fastapi import Depends, HTTPException, status
from src.repositories import UserRepository, PostRepository, LikeRepository
from src.db import database
from src.schemas import User
from src.security import JWTBearer, decode_access_token


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_post_repository() -> PostRepository:
    return PostRepository(database)


def get_like_repository() -> LikeRepository:
    return LikeRepository(database)


async def get_current_user(
    users: UserRepository = Depends(get_user_repository),
    token: str = Depends(JWTBearer()),
) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception

    email: str = payload.get("sub")
    if email is None:
        raise cred_exception

    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user
