from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import config


def init_cors(app: FastAPI):
    if config.app_debug:
        origins = [
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:5173",
            *config.cors_allowed_domains
        ]
    else:
        origins = [
            *config.cors_allowed_domains
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
