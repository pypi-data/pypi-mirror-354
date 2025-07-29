from typing import Optional, Union

from .models import Items, ItemStatus, ItemCategory, ItemResponse
from ..client import SyncApiClient, AsyncApiClient
from ..config import logger


class SyncItemClient(SyncApiClient):
    """
    Синхронный клиент для работы с API объявлений Авито.
    """

    def get_items(
        self,
        category: Optional[ItemCategory] = None,
        updated_at_from: Optional[str] = None,
        page: int = 1,
        per_page: int = 25,
        status: Optional[list[Union[ItemStatus, str]]] = None
    ) -> Items:
        """
        Получает список объявлений.

        Args:
            category: Идентификатор категории объявления
            updated_at_from: Фильтр больше либо равно по дате обновления/редактирования объявления в формате YYYY-MM-DD
            page: Номер страницы (целое число больше 0)
            per_page: Количество записей на странице (целое число больше 0 и меньше 100)
            status: Статусы объявлений для фильтрации

        Returns:
            Список объявлений пользователя
        """
        logger.debug(f"Запрос списка объявлений")

        params = {
            "page": page,
            "per_page": per_page,
        }

        # Преобразуем chat_types в строки, если они переданы как Enum
        if status:
            item_status_str = [ct.value if isinstance(ct, ItemStatus) else ct for ct in status]
        else:
            item_status_str = [ItemStatus.ACTIVE.value]

        if item_status_str:
            params["status"] = ",".join(item_status_str)
        if category:
            params["category"] = category
        if updated_at_from:
            params["updatedAtFrom"] = updated_at_from

        response = self._request_sync(
            method="GET",
            url="/core/v1/items",
            params=params,
        )

        return Items(**response)

    def get_item(self, user_id: int, item_id: int) -> ItemResponse:
        """
        Получает информацию о конкретном чате.

        Args:
            user_id: Идентификатор пользователя
            item_id: Идентификатор объявления

        Returns:
            Информация об объявлении
        """
        logger.debug(f"Запрос информации об объявлении {item_id} для пользователя {user_id}")

        response = self._request_sync(
            method="GET",
            url=f"/core/v1/accounts/{user_id}/items/{item_id}/",
        )

        return ItemResponse(**response)


class AsyncItemClient(AsyncApiClient):
    """
    Асинхронный клиент для работы с API объявлений Авито.
    """

    async def get_items(
        self,
        category: Optional[ItemCategory] = None,
        updated_at_from: Optional[str] = None,
        page: int = 1,
        per_page: int = 25,
        status: Optional[list[Union[ItemStatus, str]]] = None
    ) -> Items:
        """
        Получает список объявлений.

        Args:
            category: Идентификатор категории объявления
            updated_at_from: Фильтр больше либо равно по дате обновления/редактирования объявления в формате YYYY-MM-DD
            page: Номер страницы (целое число больше 0)
            per_page: Количество записей на странице (целое число больше 0 и меньше 100)
            status: Статусы объявлений для фильтрации

        Returns:
            Список объявлений пользователя
        """
        logger.debug(f"Запрос списка объявлений")

        params = {
            "page": page,
            "per_page": per_page,
        }

        # Преобразуем chat_types в строки, если они переданы как Enum
        if status:
            item_status_str = [ct.value if isinstance(ct, ItemStatus) else ct for ct in status]
        else:
            item_status_str = [ItemStatus.ACTIVE.value]

        if item_status_str:
            params["status"] = ",".join(item_status_str)
        if category:
            params["category"] = category
        if updated_at_from:
            params["updatedAtFrom"] = updated_at_from

        response = await self._request_async(
            method="GET",
            url="/core/v1/items",
            params=params,
        )
        return Items(**response)

    async def get_item(self, user_id: int, item_id: int) -> ItemResponse:
        """
        Получает информацию о конкретном чате.

        Args:
            user_id: Идентификатор пользователя
            item_id: Идентификатор объявления

        Returns:
            Информация об объявлении
        """
        logger.debug(f"Запрос информации об объявлении {item_id} для пользователя {user_id}")

        response = await self._request_async(
            method="GET",
            url=f"/core/v1/accounts/{user_id}/items/{item_id}/",
        )

        return ItemResponse(**response)
