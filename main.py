from fastapi import FastAPI
from app.routes import apis
from app.routes.endpoints.dynamic_router import create_dynamic_routes
from app.utils.config import ROOT_DIR
from app.utils.logger import setup_logging


# Initialize logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(title="Dynamic File-Based API", version="1.0.0")

# Root directory for resources
app.include_router(apis.router)


# Add dynamic routes
create_dynamic_routes(app, ROOT_DIR)




@app.get("/")
async def root():
    return {"message": "Welcome to the Dynamic File-Based API"}
