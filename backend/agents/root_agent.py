import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import ParallelAgent, SequentialAgent
from google.adk.tools import AgentTool

from agents.topic_agent import topic_agent
from agents.script_agent import script_agent
from agents.narrator_agent import narrator_agent
from agents.slide_agent import slide_agent
from agents.video_compiler_agent import video_compiler_agent

load_dotenv()

INSTRUCTIONS = """
You are the Orchestrator.

Your task is:

1. Receive the user's input text.
2. Invoke the pipeline tool.
3. The pipeline will automatically:
   - run topic_agent to extract the topic
   - run script_agent to generate the script
   - run slide_agent using the script and topic
   - run narrator_agent using the script and topic
   - run video_compiler_agent using the slide paths and audio path
4. When narrator_agent returns the MP3 file path, your FINAL MESSAGE
   must contain ONLY that file path — no quotes, no JSON, no explanation.

Example final output:
/app/data/speeches/basic_algebra.mp3
"""


# -------------------------------
# PARALLEL BLOCK 1: topic + script
# -------------------------------
topic_and_script = ParallelAgent(
    sub_agents=[
        topic_agent,
        script_agent
    ],
    name="parallel_topic_script"
)

# ---------------------------------------
# PARALLEL BLOCK 2: slides + narration
# ---------------------------------------
slides_and_narration = ParallelAgent(
    sub_agents=[
        slide_agent,
        narrator_agent
    ],
    name="parallel_slides_narration"
)

# ---------------------------------------------------
# SEQUENTIAL PIPELINE: (parallel1 → parallel2 → video)
# ---------------------------------------------------
pipeline = SequentialAgent(
    sub_agents=[
        topic_and_script,         # Step 1: Parallel topic + script
        slides_and_narration,     # Step 2: Parallel slides + narration
        video_compiler_agent      # Step 3: Compile into final video
    ],
    name="sequential_pipeline"
)

# ------------------------
# ORCHESTRATOR (root agent)
# ------------------------
root_agent = Agent(
    model=os.getenv("MODEL_TEXT"),
    name="RootAgent",
    description="Runs the pipeline in order to generate the final video.",
    instruction=INSTRUCTIONS,
    # IMPORTANT: pipeline becomes the ONLY “tool” used by root_agent
    tools=[
        AgentTool(agent=pipeline)
    ]
)
