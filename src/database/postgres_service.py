from sqlalchemy import insert, select
from src.database import async_session_maker
from src.database.models import User


class PostgresManager:
    async def add_user(
        self, telegram_id: int, username: str, first_name: str, last_name: str, bio: str
    ) -> None:
        async with async_session_maker() as session:
            stm = insert(User).values(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                bio=bio,
            )

            await session.execute(stm)
            await session.commit()

    async def user_exists(self, telegram_id: int) -> bool:
        async with async_session_maker() as session:
            query = select(User).where(User.telegram_id == telegram_id)

            result = await session.execute(query)
            exists = result.mappings().fetchall()

            return bool(exists)
