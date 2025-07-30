from fastapi import FastAPI
from app.routes import health, contexts
from cockroachdb_mcp_server import __version__

app = FastAPI(title="CockroachDB MCP Server", version={__version__})

app.include_router(health.router)
app.include_router(contexts.router, prefix="/contexts")


@app.get("/")
def root():
    return {"message": "MCP Server is running"}
