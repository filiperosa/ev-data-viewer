from fastapi import FastAPI
import uvicorn

from server import __version__, models
from server.database import engine
import server.routers as routers

from fastapi_pagination import add_pagination

# Initialize database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Volteras Code Challenge API",
    version=__version__,
    description="Data store API for Volteras Code Challenge",
    root_path="/api/v1"
)

# Add pagination to the app
add_pagination(app)

# Add routers as different sections of the swagger page
app.include_router(routers.vehicles_router, tags=["Vehicles"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)