from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from server import __version__, models
from server.database import engine
import server.router as router

import server.authentication as auth

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


@app.get("/users/me")
async def read_users_me(current_user: auth.User = Depends(auth.get_current_user)):
    """Get the current user object"""
    return current_user


@app.post("/token", response_model=auth.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get an access token with a username and password"""
    return auth.token_login(form_data)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)