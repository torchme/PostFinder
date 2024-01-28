from sqlalchemy import insert, select, update
from src.database import async_session_maker
from src.database.models import User, Action


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

    async def add_action(
        self,
        telegram_id: int,
        response_id: int,
        platform_type: str,
        resource_name: str,
        query: str,
        prompt: str,
        response: str,
        input_tokens: int,
        output_tokens: int,
        execution_time: int,
    ):
        async with async_session_maker() as session:
            stm = insert(Action).values(
                telegram_id=telegram_id,
                response_id=response_id,
                platform_type=platform_type,
                resource_name=resource_name,
                query=query,
                prompt=prompt,
                response=response,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                execution_time=execution_time,
            )

            await session.execute(stm)
            await session.commit()

    async def add_feedback(self, response_id: int, feedback: str):
        async with async_session_maker() as session:
            stm = (
                update(Action)
                .where(Action.response_id == response_id)
                .values(feedback=feedback)
            )

            await session.execute(stm)
            await session.commit()

    async def get_previous_context(self, reply_to_message_id: int):
        async with async_session_maker() as session:
            query = select(Action.prompt, Action.response, Action.resource_name).where(
                Action.response_id == reply_to_message_id
            )

            result = await session.execute(query)
            previus_context = result.mappings().fetchone()

            return previus_context
