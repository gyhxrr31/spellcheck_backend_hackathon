from nlp_server.app.schemas.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class SearchDictionary(Base):
    __tablename__ = "search_dictionary"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True)
    term: Mapped[str] = mapped_column(String(255))
    frequency: Mapped[int] = mapped_column(Integer)