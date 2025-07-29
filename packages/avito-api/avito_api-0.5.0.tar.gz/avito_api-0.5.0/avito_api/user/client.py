from .models import UserAccount
from ..client import SyncApiClient, AsyncApiClient
from ..config import logger


class SyncUserClient(SyncApiClient):
    """
    Синхронный клиент для работы с API пользователя Авито.
    """

    def get_account(self) -> UserAccount:
        """
        Получает информацию об авторизованном пользователе

        Returns:
            Возвращает идентификатор пользователя и его регистрационные данные.
        """
        logger.debug(f"Запрос информации об авторизованном пользователе")

        response = self._request_sync(
            method="GET",
            url=f"/core/v1/accounts/self",
        )

        return UserAccount(**response)



class AsyncUserClient(AsyncApiClient):
    """
    Асинхронный клиент для работы с API пользователя Авито.
    """

    async def get_account(self) -> UserAccount:
        """
        Получает информацию об авторизованном пользователе

        Returns:
            Возвращает идентификатор пользователя и его регистрационные данные.
        """
        logger.debug(f"Запрос информации об авторизованном пользователе")

        response = await self._request_async(
            method="GET",
            url=f"/core/v1/accounts/self",
        )

        return UserAccount(**response)
