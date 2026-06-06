import uvicorn
from fastapi import FastAPI
import os
import sys

# Add root directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from admin_backend.controllers.blog_controller import router as blog_router

app = FastAPI(title="SpacePoint Admin API")

from fastapi.staticfiles import StaticFiles

# Include the blog routes first so they take precedence
app.include_router(blog_router)

# Mount the root directory to serve the public website (index.html, blog.html, assets, etc.)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.mount("/", StaticFiles(directory=root_dir, html=True), name="public_site")

if __name__ == "__main__":
    # Run the server
    print("[SpacePoint Admin Server] Starting on http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
