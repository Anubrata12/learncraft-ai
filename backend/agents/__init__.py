import os
import sys
from pathlib import Path

# Get the directory of the current file (backend/agents)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up twice to reach the project root (learncraft-ai/)
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

# 1. Import your actual agent
from .agent import root_agent