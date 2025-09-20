from nlp_server.app.schemas.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, JSON, TIMESTAMP


class QueryHistory(Base):
    __tablename__ = "query_history"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True)
    original_query: Mapped[str] = mapped_column(String)
    processed_query: Mapped[str] = mapped_column(String)
    intent: Mapped[str] = mapped_column(String(50))
    extracted_entities: Mapped[dict] = mapped_column(JSON)
    system_action: Mapped[str] = mapped_column(String)
    result_count: Mapped[int] = mapped_column(Integer)
    satisfaction_rating: Mapped[int] = mapped_column(Integer)
    create_at: Mapped[str] = mapped_column(TIMESTAMP)

