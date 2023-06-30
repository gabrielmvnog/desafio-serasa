from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.users.exceptions import ConflictException, UserNotFounException
from app.users.models import User
from app.users.schemas import UserIn, UserOut


def list_users(db: Session, skip: int = 0, limit: int = 10) -> list[UserOut | None]:
    return db.query(User).offset(skip).limit(limit).all()


def detail_user(db: Session, user_id: int) -> User:
    try:
        db_user = db.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        raise UserNotFounException from None

    return UserOut.from_orm(db_user)


def create_user(db: Session, user_in: UserIn, user_id: int) -> UserOut:
    user_in_data = jsonable_encoder(user_in)
    db_user = User(id=user_id, **user_in_data)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as err:
        if "UniqueViolation" in err.args[0]:
            raise ConflictException from None

    return UserOut.from_orm(db_user)


def update_user(db: Session, user_in: UserIn, user_id: int) -> bool:
    user_in_data = jsonable_encoder(user_in)
    updated = db.query(User).filter(User.id == user_id).update(user_in_data)
    db.commit()

    return bool(updated)


def delete_user(db: Session, user_id: int) -> bool:
    deleted = db.query(User).filter(User.id == user_id).delete()
    db.commit()

    return bool(deleted)
