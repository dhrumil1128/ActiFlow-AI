"""
controller.py

This file orchestrates the entire agent workflow.

It connects:
- Planner (AI reasoning)
- Schema validation
- Safety validation
- Executor (actions)

This is the main control loop of ActiFlow AI.
"""

from typing import Dict, Any
import os 
from agent.planner import GeminiPlanner
from agent.validator import ActionValidator
from agent.executer import ActionExecutor
from schemas.plan_schema import Plan
from agent.logger import ActionLogger


class AgentController:
    """
    AgentController coordinates the full lifecycle of an agent run.

    It ensures:
    - Clean separation of concerns
    - Safe execution order
    - Transparent outcomes
    """

    def __init__(self, base_directory: str):
        """
        Initialize all core components.

        Parameters:
        - base_directory: Root directory where actions are allowed
        """
        self.planner = GeminiPlanner()
        self.validator = ActionValidator(base_directory)
        self.executor = ActionExecutor()
        self.logger = ActionLogger()
        self.base_directory = base_directory

    
    def resolve_path(self, base_dir: str, path: str | None):
        if not path:
            return None

        # If already absolute, leave it
        if os.path.isabs(path):
            return path

        # Otherwise, resolve relative to base directory
        return os.path.abspath(os.path.join(base_dir, path))


    # Run Method : 
    
    def run(self, user_task: str, system_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a full agent cycle.

        Parameters:
        - user_task: What the user wants to achieve
        - system_state: Current environment snapshot

        Returns:
        - Dictionary with execution results
        """

        # 1. Ask the AI to create a plan
        raw_plan = self.planner.create_plan(
            user_task=user_task,
            system_state=system_state
        )

        # 2. Validate plan structure using schema
        validated_plan = Plan(**raw_plan)
        for action in validated_plan.actions:
            action.source = self.resolve_path(self.base_directory, action.source)
            action.destination = self.resolve_path(self.base_directory, action.destination)


        # 3. Perform runtime safety validation
        approved_actions = self.validator.validate_actions(
            validated_plan.actions
        )

        # 4. Execute approved actions
        self.executor.execute_actions(approved_actions)
        
        # Generate the logs in actions.log 
        self.logger.log_actions(approved_actions)
        

        # 5. Return execution summary
        return {
            "plan_summary": validated_plan.plan_summary,
            "actions_executed": [
                {
                    "action": action.action,
                    "source": action.source,
                    "destination": action.destination,
                    "reason": action.reason
                }
                for action in approved_actions
            ]
        }
