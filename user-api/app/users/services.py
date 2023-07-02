from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.users.exceptions import ConflictException, UserNotFounException
from app.users.models import User
from app.users.schemas import UserIn, UserOut


async def list_users(
    db: Session, skip: int = 0, limit: int = 10
) -> list[UserOut | None]:
    result = (await db.execute(select(User).offset(skip).limit(limit))).scalars().all()

    logger.info("Success on query for users")

    return result


async def detail_user(db: Session, user_id: int) -> User:
    try:
        db_user = (
            (await db.execute(select(User).filter(User.id == user_id))).scalars().one()
        )
    except NoResultFound:
        logger.warning(f"No user found for user_id:{user_id}")
        raise UserNotFounException from None

    logger.info(f"Success on select for user with user_id:{user_id}")

    return UserOut.from_orm(db_user)


async def create_user(db: Session, user_in: UserIn, user_id: int) -> UserOut:
    user_in_data = jsonable_encoder(user_in)
    db_user = User(id=user_id, **user_in_data)

    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError as err:
        if "UniqueViolation" in err.args[0]:
            logger.warning(f"Conflict trying to insert user with user_id:{user_id}")
            raise ConflictException from None

    logger.info(f"Success on insert for user with user_id:{user_id}")

    return UserOut.from_orm(db_user)


async def update_user(db: Session, user_in: UserIn, user_id: int) -> bool:
    user_in_data = jsonable_encoder(user_in)

    query = update(User).where(User.id == user_id).values(**user_in_data)
    result = await db.execute(query)

    await db.commit()

    updated = bool(result.rowcount)

    if updated:
        logger.info(f"Success on update for user with user_id:{user_id}")
    else:
        logger.info(f"User not found to update with user_id:{user_id}")

    return updated


async def delete_user(db: Session, user_id: int) -> bool:
    query = delete(User).filter(User.id == user_id)
    result = await db.execute(query)

    await db.commit()

    deleted = bool(result.rowcount)

    if deleted:
        logger.info(f"Success on delete user with user_id:{user_id}")
    else:
        logger.info(f"User not found to delete with user_id:{user_id}")

    return deleted
