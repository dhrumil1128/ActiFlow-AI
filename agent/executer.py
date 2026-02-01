"""
executor.py

This file is responsible for executing actions that have already been:
- Planned by the AI
- Validated by schemas
- Approved by safety checks

IMPORTANT:
- This file contains NO AI logic
- It simply performs deterministic file system operations
"""

import os
import shutil
from typing import List

from schemas.action_schema import Action


class ActionExecutor:
    """
    ActionExecutor performs the actual execution of approved actions.

    It assumes:
    - All actions are safe
    - All actions are valid
    """

    def execute_actions(self, actions: List[Action]) -> None:
        """
        Execute a list of approved actions sequentially.

        Parameters:
        - actions: List of Action objects
        """
        for action in actions:
            if action.action == "no_action":
                # Explicitly do nothing
                continue

            if action.action == "create_folder":
                self._create_folder(action)

            elif action.action == "move_file":
                self._move_file(action)

            elif action.action == "rename_file":
                self._rename_file(action)

            else:
                # This should never happen if validation is correct
                raise ValueError(f"Unsupported action type: {action.action}")

    def _create_folder(self, action: Action) -> None:
        """
        Create a folder at the destination path.

        Uses exist_ok=True to avoid crashing
        if the folder already exists.
        """
        if not action.destination:
            raise ValueError("Missing destination for create_folder action")

        os.makedirs(action.destination, exist_ok=True)
        

    def _move_file(self, action: Action) -> None:
        """
        Move a file from source to destination.
        """
        if not action.source or not action.destination:
            raise ValueError("move_file action requires source and destination")

        shutil.move(action.source, action.destination)
        

    def _rename_file(self, action: Action) -> None:
        """
        Rename a file from source to destination.
        """
        if not action.source or not action.destination:
            raise ValueError("rename_file action requires source and destination")

        os.rename(action.source, action.destination)
