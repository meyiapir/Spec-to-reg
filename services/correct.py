from sqlalchemy.exc import SQLAlchemyError

from database.models import CorrectModel
from sqlalchemy.ext.asyncio import AsyncSession


async def record_correct(session: AsyncSession, comment: str = None) -> None:
    try:
        correct = CorrectModel(comment=comment)

        session.add(correct)

        await session.commit()

    except SQLAlchemyError as _ex:
        await session.rollback()
        print(f"Smth went wrong: {_ex}")

    finally:
        await session.close()
