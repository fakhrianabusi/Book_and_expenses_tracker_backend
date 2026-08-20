from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from settings.general_settings import general_settings

engine = create_engine(
    general_settings.DATABASE_URL,
    echo=general_settings.ECHO,
    connect_args={"check_same_thread": False}
    if "sqlite" in general_settings.DATABASE_URL
    else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    author: Mapped[str]
    amount: Mapped[int]
    price: Mapped[float]


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    amount: Mapped[int]
    price: Mapped[float]
    category: Mapped[str] = mapped_column(default="General")


def create_db_tables():
    Base.metadata.create_all(bind=engine)


def seed_db():
    db = SessionLocal()
    if not db.query(BookModel).first():
        db.add(
            BookModel(
                title="Clean Code", author="Robert C. Martin", amount=1, price=29.99
            )
        )
        db.commit()
    db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
