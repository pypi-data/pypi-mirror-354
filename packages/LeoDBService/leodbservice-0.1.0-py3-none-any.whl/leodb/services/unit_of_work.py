from __future__ import annotations
import abc
from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.general.account import Account
from leodb.models.general.user import User
from leodb.repositories.user_repository import UserRepository
from leodb.repositories.account_repository import AccountRepository
# Import other repositories here as they are created

class AbstractUnitOfWork(abc.ABC):
    users: UserRepository
    accounts: AccountRepository
    # Define other repositories here

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.users = UserRepository(self._session, User)
        self.accounts = AccountRepository(self._session, Account)
        # Instantiate other repositories here

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()