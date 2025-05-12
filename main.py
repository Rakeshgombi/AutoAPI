from fastapi import FastAPI
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time
from starlette.middleware.cors import CORSMiddleware

from routes import apis
from routes.endpoints.dynamic_router import create_dynamic_routes
from utils.config import ROOT_DIR
from utils.logger import setup_logging

# Initialize logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(title="AutoAPI", description="Dynamic File-Based APIs", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root directory for resources
app.include_router(apis.router)

# Add dynamic routes
create_dynamic_routes(app, ROOT_DIR)


class DataFolderEventHandler(FileSystemEventHandler):
    """Handles changes in the /data folder."""

    def on_any_event(self, event):
        if event.event_type in {"created", "deleted", "modified", "moved"}:
            try:
                # Preserve default routes (like /docs and /openapi.json)
                default_routes = [
                    route
                    for route in app.router.routes
                    if route.path in ["/docs", "/openapi.json", "/redoc", "/"]
                ]

                # Clear existing routes and re-add default routes
                app.router.routes.clear()
                app.router.routes.extend(default_routes)

                # Re-add static and dynamic routes
                app.include_router(apis.router)
                create_dynamic_routes(app, ROOT_DIR)

                # Reset OpenAPI schema to refresh Swagger UI
                app.openapi_schema = None
                print(
                    f"Routes and OpenAPI schema refreshed due to {event.event_type} event."
                )
            except Exception as e:
                print(f"Error refreshing routes: {e}")


def start_watcher():
    """Start the watchdog observer to monitor the /data folder."""
    event_handler = DataFolderEventHandler()
    observer = Observer()
    observer.schedule(event_handler, ROOT_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Start the folder watcher in a separate thread
threading.Thread(target=start_watcher, daemon=True).start()


@app.get("/")
async def root():
    return {"message": "Welcome to the Dynamic File-Based API"}
