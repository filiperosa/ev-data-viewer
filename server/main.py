from fastapi import FastAPI, Depends, HTTPException
import uvicorn

from server import __version__, models
from server.database import engine
import server.router as router

from server.authentication import get_current_active_user, User, UserInDB, OAuth2PasswordRequestForm, fake_users_db, fake_hash_password

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
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)