import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(expenses_router)
app.include_router(books_router)


@app.get("/")
def hello_world():
    return {"Hello": "World"}
