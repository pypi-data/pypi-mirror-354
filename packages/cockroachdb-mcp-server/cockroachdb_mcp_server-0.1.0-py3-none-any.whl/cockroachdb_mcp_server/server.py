import uvicorn


def start_server(host: str = "0.0.0.0", port: int = 8081, reload: bool = False):
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
