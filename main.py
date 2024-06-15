from fastapi import FastAPI
from database.db import Base, engine
from routes.contacts import router as contacts_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(contacts_router, prefix="/contacts")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
