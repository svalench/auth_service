from fastapi import FastAPI
from route import protected_user_model, router


app = FastAPI()


app.include_router(protected_user_model)
app.include_router(router)


