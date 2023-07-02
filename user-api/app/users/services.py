from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.users.exceptions import ConflictException, UserNotFounException
from app.users.models import User
from app.users.schemas import UserIn, UserOut


async def list_users(
    db: Session, skip: int = 0, limit: int = 10
) -> list[UserOut | None]:
    return (await db.execute(select(User).offset(skip).limit(limit))).scalars().all()


async def detail_user(db: Session, user_id: int) -> User:
    try:
        db_user = (
            (await db.execute(select(User).filter(User.id == user_id))).scalars().one()
        )
    except NoResultFound:
        raise UserNotFounException from None

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
            raise ConflictException from None

    return UserOut.from_orm(db_user)


async def update_user(db: Session, user_in: UserIn, user_id: int) -> bool:
    user_in_data = jsonable_encoder(user_in)

    query = update(User).where(User.id == user_id).values(**user_in_data)
    updated = await db.execute(query)

    await db.commit()

    return bool(updated.rowcount)


async def delete_user(db: Session, user_id: int) -> bool:
    query = delete(User).filter(User.id == user_id)
    deleted = await db.execute(query)

    await db.commit()

    return bool(deleted.rowcount)
