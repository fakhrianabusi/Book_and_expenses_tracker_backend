import contextlib

from fastapi import FastAPI

from database import create_db_tables, seed_db
from router.books import router as books_router
from router.expenses import router as expenses_router
from settings.general_settings import general_settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_tables()
    seed_db()
    yield
    print("#################################")
    print("APPLICATION SHUTDOWN")
    print("#################################")
    # Shutdown code


app = FastAPI(
    title=general_settings.APP_TITLE,
    version=general_settings.VERSION,
    lifespan=lifespan,
)


app.include_router(expenses_router)
app.include_router(books_router)


@app.get("/")
def hello_world():
    return {"Hello": "World"}
