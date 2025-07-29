from xync_schema import models


async def main():
    from os import getenv as env
    from dotenv import load_dotenv
    import logging
    from x_model import init_db
    from logging import DEBUG

    load_dotenv()
    logging.basicConfig(level=DEBUG)
    await init_db(env("DB_URL"), models, True)


if __name__ == "__main__":
    from asyncio import run

    run(main())


1 + 3
3 + 3
4 + 3
5 + 3
6 + 3
8 + 3
9 + 3
10 + 3
11 + 3
12 + 3
13 + 3
14 + 3
15 + 3
16 + 3
18 + 3
20 + 3
21 + 3
22 + 3
24 + 3
25 + 3
26 + 3
27 + 3
28 + 3
29 + 3
30 + 3
31 + 3
32 + 3
34 + 3
