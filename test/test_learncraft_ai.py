from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest
from pathlib import Path

DIR = Path(__file__).resolve().parent
EVAL_FILE = DIR/"integration.evalset.json"   # test/integration.evalset.json

@pytest.mark.asyncio
async def test_with_single_test_file():
    """Test the agent's basic ability via a session file."""
    print("*******************************: ", EVAL_FILE)

    await AgentEvaluator.evaluate(
        agent_module="backend.agents",
        eval_dataset_file_path_or_dir=str(EVAL_FILE),
    )


