from fastapi import FastAPI
from agents.orchestrator import run_agent
from agents.speeches_agent.narrator import synthesize_via_agent


app = FastAPI()

@app.get("/generate")
def generate(topic: str):
    return {"response": run_agent(topic)}

@app.get("/narrate")
def narrate_script():
    audio_file = synthesize_via_agent()
    return {"file": audio_file}  # absolute path
