from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import sessionmaker
from services.mistakes import collect_reasons

router = APIRouter(prefix="/results")


async def get_session():
    async with sessionmaker() as session:
        yield session


@router.get("/reasons")
async def credentials(session: AsyncSession = Depends(get_session)):
    reasons = await collect_reasons(session)

    return reasons
