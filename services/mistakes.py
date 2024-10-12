from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import MistakesModel
from sqlalchemy.ext.asyncio import AsyncSession


async def record_mistake(session: AsyncSession, reason: str) -> None:
    try:
        mistake = MistakesModel(reason=reason)

        session.add(mistake)

        await session.commit()

    except SQLAlchemyError as _ex:
        await session.rollback()
        print(f"Smth went wrong: {_ex}")

    finally:
        await session.close()


async def collect_reasons(session: AsyncSession) -> list[MistakesModel.reason]:
    query = select(MistakesModel.created_at, MistakesModel.reason).limit(500000)

    result = await session.execute(query)
    rows = result.fetchall()

    return rows
