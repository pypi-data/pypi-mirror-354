"""
Модели данных для модуля мессенджера API Авито.
"""
from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional

from pydantic import BaseModel, Field


class VasId(str, Enum):
    """ Идентификатор услуги """
    VIP = "vip"
    HIGHLIGHT = "highlight"
    PUSHUP = "pushup"
    PREMIUM = "premium"
    XL = "xl"


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


class ItemCategoryResponse(BaseModel):
    id: int = Field(..., description="id категории объявлений")
    name: str = Field(..., description="название категории объявлений")


# Модели запросов
class ItemMeta(BaseModel):
    """Метаинформация объявлений."""

    page: int = Field(..., description="Номер страницы")
    per_page: int = Field(..., description="Количество записей на странице")


class Item(BaseModel):
    """Модель объявления в списке объявлений."""

    id: int = Field(..., description="Идентификатор объявления")
    address: str = Field(..., description="Адрес объявления")
    category: ItemCategoryResponse = Field(..., description="категория объявления")
    price: Optional[int] = Field(None, description="Цена объявления (null значение означает, что цена не указана)")
    status: ItemStatus = Field(..., description="Статус объявления на сайте")
    title: str = Field(..., description="Наименование объявления")
    url: Optional[str] = Field(None, description="URL-адрес объявления")


class Items(BaseModel):
    """Список объявлений."""
    meta: ItemMeta = Field(..., description="Метаинформация")
    resources: list[Item] = Field(..., description="Список объявлений")


class InfoVas(BaseModel):
    """ Данные по доп. услуге """
    vas_id: VasId = Field(..., description="Идентификатор услуги")
    schedule: Optional[list[str]] = Field(None, description="Информация о следующих применениях услуги")
    finish_time: Optional[datetime] = Field(None, description="Дата завершения услуги")


class ItemResponse(BaseModel):
    """Модель объявления."""
    autoload_item_id: Optional[str] = Field(None, description="Идентификатор объявления из файла автозагрузки")
    start_time: Optional[datetime] = Field(None, description="Дата создания объявления")
    finish_time: Optional[datetime] = Field(None, description="Дата завершения объявления")
    status: ItemStatus = Field(..., description="Статус объявления на сайте")
    url: Optional[str] = Field(None, description="URL-адрес объявления")
    vas: Optional[list[InfoVas]] = Field(None, description="Список дополнительных услуг")
