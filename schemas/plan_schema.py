"""
plan_schema.py

This file defines the schema for an AI-generated execution plan.

A Plan represents the complete intent of the agent,
including a summary and a list of validated actions.
"""

from typing import List
from pydantic import BaseModel, Field

from schemas.action_schema import Action


class Plan(BaseModel):
    """
    Plan represents a full plan created by the AI planner.

    It contains:
    - A short summary explaining the intent
    - A list of actions to be executed
    """

    plan_summary: str = Field(
        ...,
        description="High-level summary of what the agent intends to do"
    )

    actions: List[Action] = Field(
        ...,
        description="Ordered list of actions proposed by the agent"
    )
