# Справочник API: Модуль пользователя

Модуль `avito_api.user` предоставляет классы и модели для работы с API пользователя Авито.

## Клиенты пользователя

### SyncUserClient

```python
from avito_api.user import SyncUserClient
```

Синхронный клиент для работы с API пользователя Авито.

#### Пример использования

```python
from avito_api.user import SyncUserClient

user_client = SyncUserClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получить информацию о пользователе
user = user_client.get_account()
print(f"Пользователь: {user}")
```

#### Основные методы

```python
    def get_account(self) -> UserAccount:
        """
        Получает информацию об авторизованном пользователе

        Returns:
            Возвращает идентификатор пользователя и его регистрационные данные.
        """
```

### AsyncUserClient

```python
from avito_api.user import AsyncUserClient
```

Асинхронный клиент для работы с API пользователя Авито.

#### Пример использования

```python
import asyncio
from avito_api.user import AsyncUserClient

async def main():
    user_client = AsyncUserClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получить информацию о пользователе
    user = await user_client.get_account()

    print(f"Пользователь: {user}")

asyncio.run(main())
```

Класс `AsyncUserClient` предоставляет те же методы, что и `SyncUserClient`, но в асинхронной форме. Все методы начинаются с `async def` и должны вызываться с `await`.
