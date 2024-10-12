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
