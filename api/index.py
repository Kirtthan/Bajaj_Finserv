from app.main import app
from mangum import Mangum  # Mangum adapts ASGI (FastAPI) to AWS Lambda/Vercel

handler = Mangum(app)
