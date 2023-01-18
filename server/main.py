from fastapi import FastAPI
import uvicorn

from server import __version__
import server.routers as routers

app = FastAPI(
    title="Volteras Code Challenge API",
    version=__version__,
    description="Data store API for Volteras Code Challenge"
)


# Add routers as different sections of the swagger page
app.include_router(routers.default_router, tags=["Default"])