from pydantic import BaseModel, Field


class UserAccount(BaseModel):
    """Информация о пользователе."""

    id: int = Field(..., description="ID пользователя")
    name: str = Field(..., description="Имя пользователя")
    email: str = Field(..., description="Email пользователя")
    phone: str = Field(..., description="первый верифицированный телефон пользователя")
    phones: list[str] = Field(..., description="все верифицированные номера телефонов")
    profile_url: str = Field(..., description="Ссылка на профиль пользователя")
