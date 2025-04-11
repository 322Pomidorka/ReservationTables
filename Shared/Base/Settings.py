from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: str
    url: str


@dataclass
class Config:
    database: DbConfig


def get_settings():
    path = '.env'
    env = Env()
    env.read_env(path)

    return Config(
        database=DbConfig(
            host=env.str('DB_LB_HOST'),
            password=env.str('DB_PASSWORD'),
            user=env.str('DB_USER'),
            database=env.str('POSTGRES_DB'),
            port=env.str('DB_LB_PORT'),
            url=f"postgresql+asyncpg://{env.str('DB_USER')}:{env.str('DB_PASSWORD')}@{env.str('DB_LB_HOST')}:{env.str('DB_LB_PORT')}/{env.str('POSTGRES_DB')}",
        ),
    )


Settings = get_settings()
