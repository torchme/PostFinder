from sqlalchemy import insert, select, update, delete
from src.database import async_session_maker
from src.database.models import User, Action, Channel


class PostgresManager:
    async def add_user(
        self, telegram_id: int, username: str, first_name: str, last_name: str, bio: str
    ) -> None:
        """
        Add a new user to the database with the provided Telegram ID, username, first name, last name, and bio.

        Parameters
        ----------
        telegram_id : int
            The Telegram ID of the user.
        username : str
            The username of the user.
        first_name : str
            The first name of the user.
        last_name : str
            The last name of the user.
        bio : str
            The bio of the user
        """
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

    async def del_user(self, telegram_id: int) -> None:
        async with async_session_maker() as session:
            stm = delete(User).where(User.telegram_id == telegram_id)
            await session.execute(stm)
            await session.commit()

    async def user_exists(self, telegram_id: int) -> bool:
        """
        Check if a user with the given telegram_id exists in the database.

        Parameters
        ----------
        self : instance
            The instance of the class.
        telegram_id : int
            The telegram_id of the user to check.

        Returns
        -------
        bool
            True if the user exists, False otherwise.
        """
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
        """
        Add a new action to the database with the provided Telegram ID, response ID, platform type, resource name, query, prompt, response, input tokens, output tokens, and execution time.

        Parameters
        ----------
        telegram_id : int
            The Telegram ID of the user.
        response_id : int
            The response ID of the action.
        platform_type : str
            The platform type of the action.
        resource_name : str
            The name of the resource.
        query : str
            The query of the action.
        prompt : str
            The prompt of the action.
        response : str
            The response of the action.
        input_tokens : int
            The number of input tokens of the action.
        output_tokens : int
            The number of output tokens of the action.
        execution_time : int
            The execution time of the action.
        """
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
        """
        Add a new feedback to the database with the provided response ID and feedback.

        Parameters
        ----------
        response_id : int
            The response ID of the action.
        feedback : str
            The feedback of the user.
        """
        async with async_session_maker() as session:
            stm = (
                update(Action)
                .where(Action.response_id == response_id)
                .values(feedback=feedback)
            )

            await session.execute(stm)
            await session.commit()

    async def get_previous_context(self, reply_to_message_id: int):
        """
        Get the previous context from the database with the provided reply_to_message_id.

        Parameters
        ----------
        reply_to_message_id : int
            The reply_to_message_id of the action.

        Returns
        -------
        previus_context
        """
        async with async_session_maker() as session:
            query = select(Action.prompt, Action.response, Action.resource_name).where(
                Action.response_id == reply_to_message_id
            )

            result = await session.execute(query)
            previus_context = result.mappings().fetchone()

            return previus_context

    async def add_channel(
        self, channel: str, user_id: int, members_count: int, username: str
    ) -> None:
        """
        Add channel to pool.

        Parameters
        ----------
        channel:
            Channel to add.
        """
        async with async_session_maker() as session:
            stm = insert(Channel).values(
                channel=channel,
                requested_by_id=user_id,
                username=username,
                followers_count=members_count,
            )

            await session.execute(stm)
            await session.commit()
            return True

    async def del_channel(self, channel: str):
        async with async_session_maker() as session:
            stm = delete(Channel).where(Channel.channel == channel)
            await session.execute(stm)
            await session.commit()

        return True

    async def channel_exists(self, channel: str) -> bool:
        """
        Check if a user with the given telegram_id exists in the database.

        Parameters
        ----------
        self : instance
            The instance of the class.
        channel : str
            Channel to check.

        Returns
        -------
        bool
            True if the user exists, False otherwise.
        """
        async with async_session_maker() as session:
            query = select(Channel.channel).where(Channel.channel == channel)

            result = await session.execute(query)
            exists = result.mappings().fetchall()

            return bool(exists)

    async def get_pool(self) -> tuple[str, str, str]:
        """
        Return the pool of channels.

        Parameters
        ----------
        self : instance
            The instance of the class.

        Returns
        -------
        tuple[str, str, int]
            (channel:str, username:str, followers:int)
        """
        async with async_session_maker() as session:
            query = select(
                Channel.channel, Channel.username, Channel.followers
            ).order_by()

            result = await session.execute(query)
            result = result.all()
            return result
