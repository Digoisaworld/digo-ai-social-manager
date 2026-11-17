from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Text, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from app.config import get

engine = create_engine(get("DATABASE_URL", "sqlite:///./digo_social.db"), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class PublishedPost(Base):
    __tablename__ = "published_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    topic: Mapped[str] = mapped_column(String(300))
    telegram_text: Mapped[str] = mapped_column(Text)
    x_text: Mapped[str] = mapped_column(Text)
    source_urls: Mapped[str] = mapped_column(Text, default="")
    image_path: Mapped[str] = mapped_column(String(500), default="")
    telegram_message_id: Mapped[str] = mapped_column(String(100), default="")
    x_post_id: Mapped[str] = mapped_column(String(100), default="")
    content_hash: Mapped[str] = mapped_column(String(64), unique=True)

Base.metadata.create_all(engine)
