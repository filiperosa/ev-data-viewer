from fastapi import FastAPI
import uvicorn

from server import __version__, models
from server.database import engine
import server.router as router

from fastapi_pagination import add_pagination

# Initialize database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EV Data Store",
    version=__version__,
    description="Data store API for electric vehicle data",
    root_path="/api/v1"
)

# Add pagination to the app
add_pagination(app)

# Add routers as different sections of the swagger page
app.include_router(router.router, tags=["Vehicles"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)