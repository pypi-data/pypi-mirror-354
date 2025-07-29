# Справочник API: Модуль объявлений

Модуль `avito_api.item` предоставляет классы и модели для работы с API объявлений Авито.

## Клиенты объявлений

### SyncItemClient

```python
from avito_api.item import SyncItemClient
```

Синхронный клиент для работы с API объявлений Авито.

#### Пример использования

```python
from avito_api.item import SyncItemClient

item_client = SyncItemClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получить информацию об объявлении
user_id = 12345678
item_id=24421157554
item = item_client.get_item(user_id=user_id, item_id=item_id)
print(f"Объявление: {item}")
```

#### Основные методы

```python
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

    def get_item(self, user_id: int, item_id: int) -> ItemResponse:
        """
        Получает информацию о конкретном чате.

        Args:
            user_id: Идентификатор пользователя
            item_id: Идентификатор объявления

        Returns:
            Информация об объявлении
        """
```

### AsyncMessengerClient

```python
from avito_api.item import AsyncItemClient
```

Асинхронный клиент для работы с API объявлений Авито.

#### Пример использования

```python
import asyncio
from avito_api.item import AsyncItemClient

async def main():
    item_client = AsyncItemClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получить информацию об объявлении
    user_id = 12345678
    item_id=24421157554
    item = await item_client.get_item(user_id=user_id, item_id=item_id)

    print(f"Объявление: {item}")

asyncio.run(main())
```

Класс `AsyncItemClient` предоставляет те же методы, что и `SyncItemClient`, но в асинхронной форме. Все методы начинаются с `async def` и должны вызываться с `await`.

## Enum-типы данных

### ChatType

```python
from avito_api.item import ItemStatus
```

Enum-класс для статуса объявления.

```python
class ItemStatus(str, Enum):
    """Статус объявления на сайте."""
    ACTIVE = "active"
    REMOVED = "removed"
    OLD = "old"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    NOT_FOUND = "not_found"
    ANOTHER_USER = "another_user"

    @property
    def label(self) -> str:
        return {
            "active": "Активно",
            "removed": "Удалено",
            "old": "Архив",
            "blocked": "Заблокировано",
            "rejected": "Отклонено",
            "not_found": "Не найдено",
            "another_user": "Другой пользователь",
        }[self.value]
```

### MessageType

```python
from avito_api.item import ItemCategory
```

Enum-класс идентификаторов категорий объявлений.

```python
class ItemCategory(IntEnum):
    AUTOMOBILES = 9
    MOTORCYCLES = 14
    TRUCKS_SPECIAL = 81
    WATER_TRANSPORT = 11
    PARTS_ACCESSORIES = 10
    FLATS = 24
    ROOMS = 23
    HOUSES = 25
    LAND = 26
    GARAGES = 85
    COMMERCIAL_REALTY = 42
    REALTY_ABROAD = 86
    RENTAL_HOUSING = 338
    VACANCIES = 111
    RESUMES = 112
    SERVICES = 114
    CLOTHING = 27
    CHILD_CLOTHING = 29
    TOYS = 30
    WATCHES_JEWELRY = 28
    BEAUTY_HEALTH = 88
    HOME_APPLIANCES = 21
    FURNITURE = 20
    KITCHEN = 87
    REPAIR_BUILD = 19
    PLANTS = 106
    AUDIO_VIDEO = 32
    GAMES = 97
    DESKTOPS = 31
    LAPTOPS = 98
    OFFICE_EQUIPMENT = 99
    TABLETS = 96
    PHONES = 84
    COMPUTER_ACCESSORIES = 101
    PHOTO = 105
    TICKETS = 33
    BICYCLES = 34
    BOOKS = 83
    COLLECTIBLES = 36
    MUSICAL_INSTRUMENTS = 38
    HUNTING_FISHING = 102
    SPORT = 39
    DOGS = 89
    CATS = 90
    BIRDS = 91
    AQUARIUM = 92
    OTHER_ANIMALS = 93
    ANIMAL_PRODUCTS = 94
    READY_BUSINESS = 116
    BUSINESS_EQUIPMENT = 40

    @property
    def label(self) -> str:
        labels = {
            9: "Автомобили",
            14: "Мотоциклы и мототехника",
            81: "Грузовики и спецтехника",
            11: "Водный транспорт",
            10: "Запчасти и аксессуары",
            24: "Квартиры",
            23: "Комнаты",
            25: "Дома, дачи, коттеджи",
            26: "Земельные участки",
            85: "Гаражи и машиноместа",
            42: "Коммерческая недвижимость",
            86: "Недвижимость за рубежом",
            338: "Аренда жилья",
            111: "Вакансии",
            112: "Резюме",
            114: "Предложение услуг",
            27: "Одежда, обувь, аксессуары",
            29: "Детская одежда и обувь",
            30: "Товары для детей и игрушки",
            28: "Часы и украшения",
            88: "Красота и здоровье",
            21: "Бытовая техника",
            20: "Мебель и интерьер",
            87: "Посуда и товары для кухни",
            19: "Ремонт и строительство",
            106: "Растения",
            32: "Аудио и видео",
            97: "Игры, приставки и программы",
            31: "Настольные компьютеры",
            98: "Ноутбуки",
            99: "Оргтехника и расходники",
            96: "Планшеты и электронные книги",
            84: "Телефоны",
            101: "Товары для компьютера",
            105: "Фототехника",
            33: "Билеты и путешествия",
            34: "Велосипеды",
            83: "Книги и журналы",
            36: "Коллекционирование",
            38: "Музыкальные инструменты",
            102: "Охота и рыбалка",
            39: "Спорт и отдых",
            89: "Собаки",
            90: "Кошки",
            91: "Птицы",
            92: "Аквариум",
            93: "Другие животные",
            94: "Товары для животных",
            116: "Готовый бизнес",
            40: "Оборудование для бизнеса",
        }
        return labels[self.value]
```
