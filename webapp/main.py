from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from webapp.routers import tokens, users

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")
app.include_router(tokens.router)
app.include_router(users.router)


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/ping')
def ping():
    return {'status': 'ok'}


