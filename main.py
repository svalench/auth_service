from fastapi import FastAPI, Request, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

from core.route import protected_user_model, router, protected_email_model
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.utils import get_current_username


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.mount("/core/static", StaticFiles(directory="core/static"), name="static")
templates = Jinja2Templates(directory="core/templates")


@app.get('/', response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/docs")
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json")
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title="FastAPI", version="0.1.0", routes=app.routes)

app.include_router(protected_user_model)
app.include_router(protected_email_model)
app.include_router(router)

