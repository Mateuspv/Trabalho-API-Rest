from fastapi import FastAPI, HTTPException, Request, Response
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()