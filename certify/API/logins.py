from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert

from certify.database.database import sessionmaker
from certify.database.models.logins import LoginsModel
from certify.database.schemas.credentials_schemas import CredentialsCommitRequest

router = APIRouter(prefix="/logins")


async def get_session():
    async with sessionmaker() as session:
        yield session


@router.get("/credentials")
async def credentials(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(LoginsModel))

    rows = result.scalars().all()

    creds = {"usernames": {}}

    for row in rows:
        user_data = {
            "name": row.name,
            "password": row.password,
        }
        creds["usernames"][row.username] = user_data

    return creds


@router.post("/credentials_commit")
async def commit_changes(request: CredentialsCommitRequest, session: AsyncSession = Depends(get_session)):
    try:
        async with session.begin():
            await session.execute(delete(LoginsModel))

            for username, details in request.credentials.usernames.items():
                await session.execute(insert(LoginsModel).values(
                    username=username,
                    name=details.name,
                    password=details.password
                ))

        return {"status": "success", "message": "Data committed successfully"}
    except SQLAlchemyError as _ex:
        return {"status": "error", "message": f"Something went wrong {_ex}"}
