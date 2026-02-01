"""
validator.py

This file performs runtime safety validation on actions.

Its job is to:
- Ensure actions are safe in the current environment
- Enforce path and permission rules
- Block dangerous or unintended operations

IMPORTANT:
- This file does NOT execute actions
- It only approves or rejects them
"""

import os
from typing import List

from schemas.action_schema import Action


class ActionValidator:
    """
    ActionValidator enforces safety rules before execution.

    It ensures:
    - Paths stay within the allowed base directory
    - No destructive or unsafe actions are performed
    """

    def __init__(self, base_directory: str):
        """
        Initialize the validator with a base directory.

        All actions must stay inside this directory.
        """
        self.base_directory = os.path.abspath(base_directory)

    def _is_safe_path(self, path: str) -> bool:
        """
        Check whether a path stays inside the base directory.

        This prevents directory traversal and access
        to system or unrelated files.
        """
        absolute_path = os.path.abspath(path)
        return absolute_path.startswith(self.base_directory)

    def validate_actions(self, actions: List[Action]) -> List[Action]:
        """
        Validate a list of actions.

        Parameters:
        - actions: List of Action objects (already schema-validated)

        Returns:
        - A list of approved actions

        Raises:
        - ValueError if any action is unsafe
        """
        approved_actions = []
        

        for action in actions:
            # 'no_action' is always safe
            if action.action == "no_action":
                approved_actions.append(action)
                continue
            
            
            # create_folder should NEVER have a source
            if action.action == "create_folder":
                if action.source:
                    raise ValueError("create_folder action must not have a source")


            # Validate source path if present
            if action.source:
                if not self._is_safe_path(action.source):
                    raise ValueError(
                        f"Unsafe source path detected: {action.source}"
                    )

            # Validate destination path if present
            if action.destination:
                if not self._is_safe_path(action.destination):
                    raise ValueError(
                        f"Unsafe destination path detected: {action.destination}"
                    )

            # If all checks pass, approve the action
            approved_actions.append(action)

        return approved_actions
