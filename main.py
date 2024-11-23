from typing import List

import uvicorn
from fastapi import FastAPI, Form, UploadFile, File

from routers import estimate

app = FastAPI()

app.include_router(estimate.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)