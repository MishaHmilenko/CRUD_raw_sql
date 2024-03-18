from dataclasses import dataclass


@dataclass
class APIConfig:
    host: str = '0.0.0.0'
    port: int = 8001


@dataclass
class Config:
    api: APIConfig
