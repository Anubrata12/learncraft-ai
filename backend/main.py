from fastapi import FastAPI
from agents.orchestrator import run_agent


app = FastAPI()

@app.get("/generate")
def generate(topic: str):
    return {"response": run_agent(topic)}
