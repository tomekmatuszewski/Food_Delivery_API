import uvicorn

from app.main import create_app

app = create_app()
uvicorn.run(app)
