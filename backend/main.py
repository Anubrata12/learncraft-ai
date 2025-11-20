from fastapi import FastAPI
from agents.orchestrator import run_agent
from agents import narrator  # import narrator module

app = FastAPI()

@app.get("/generate")
def generate(topic: str):
    return {"response": run_agent(topic)}

@app.get("/narrate")
async def narrate_script():
    audio_file = await narrator.synthesize()
    return {"file": str(audio_file)}
