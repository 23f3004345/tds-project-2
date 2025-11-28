from fastapi import FastAPI
from main import app

# Vercel expects the app to be named 'app' or exported as handler
handler = app