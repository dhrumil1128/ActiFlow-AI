"""
logger.py

This file handles logging for ActiFlow AI.

It records:
- What actions were taken
- Why they were taken
- When they were taken

IMPORTANT:
- This file does NOT control logic
- It only records events for transparency and auditing
"""

import json
import os
from datetime import datetime
from typing import List

from schemas.action_schema import Action


class ActionLogger:
    """
    ActionLogger writes structured logs for agent actions.

    Logs are stored as JSON lines for easy inspection
    and potential future analytics.
    """

    def __init__(self, log_file: str = "log/actions.log"):
        """
        Initialize the logger.

        Parameters:
        - log_file: Path to the log file
        """
        self.log_file = log_file

        # Ensure log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log_actions(self, actions: List[Action]) -> None:
        """
        Log a list of executed actions.

        Parameters:
        - actions: List of Action objects that were executed
        """
        timestamp = datetime.utcnow().isoformat()

        # Open the log file in append mode to write new logs at the end, without deleting old logs.
        with open(self.log_file, "a", encoding="utf-8") as f:
            for action in actions:
                log_entry = {
                    "timestamp": timestamp,
                    "action": action.action,
                    "source": action.source,
                    "destination": action.destination,
                    "reason": action.reason,
                }

                # Write each action as a single JSON line
                f.write(json.dumps(log_entry) + "\n")
