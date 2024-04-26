from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.api as api
import app.pages as pages

app = FastAPI(title="HAS Individual Inquiry System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages.router)
app.include_router(api.router)
