import pytest
from dotenv import load_dotenv
from tortoise import connections
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db

from xync_schema import TORM

load_dotenv()


@pytest.fixture
async def _dbc() -> AsyncpgDBClient:
    await init_db(TORM, True)
    cn: AsyncpgDBClient = connections.get("default")
    yield cn
    await cn.close()


async def test_init_db(_dbc):
    assert isinstance(_dbc, AsyncpgDBClient), "DB corrupt"


# async def test_models(_dbc):
#     c = await models.Ex.first()
#     assert isinstance(c, models.Ex), "No exs"
