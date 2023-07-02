from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
