"""
planner.py

This file is responsible for:
- Talking to the Gemini LLM
- Asking it to create a step-by-step plan
- Returning actions in a structured JSON format

IMPORTANT:
- This file does NOT execute any actions
- It only decides WHAT should be done, not HOW
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

 
import google.generativeai as genai


class GeminiPlanner:
    """
    GeminiPlanner is the 'thinking brain' of the agent.

    It takes:
    - A user task (natural language)
    - The current environment state (e.g. files)

    And returns:
    - A structured plan (JSON)
    """

    def __init__(self):
        load_dotenv()
        """
        Initialize Gemini configuration.

        We read the API key from environment variables
        to avoid hardcoding secrets in the code.
        """
        key = os.getenv("GEMINI_API_KEY")

        if not key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in the .env file."
            )

        # Configure Gemini SDK
        genai.configure(api_key=key)

        # Initialize the Gemini model
        self.model = genai.GenerativeModel("gemini-pro")

    def create_plan(self, user_task: str, system_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ask Gemini to create a plan.

        Parameters:
        - user_task: What the user wants (e.g. "Organize my PDFs")
        - system_state: Current environment info (files, folders, etc.)

        Returns:
        - A dictionary representing the plan and actions
        """

        # Convert system state into readable JSON for the LLM
        system_state_json = json.dumps(system_state, indent=2)

        # This prompt is CRITICAL.
        # We explicitly force Gemini to return JSON only.
        prompt = f"""
You are an AI planning agent.

Your job is to create a SAFE and CLEAR plan
to complete the user's task.

Rules:
- DO NOT execute anything
- DO NOT explain in natural language
- ONLY return valid JSON
- Actions must be from this allowed list:
  - create_folder
  - move_file
  - rename_file
  - no_action

User task:
{user_task}

Current system state:
{system_state_json}

Return JSON in this exact format:
{{
  "plan_summary": "short explanation of intent",
  "actions": [
    {{
      "action": "create_folder | move_file | rename_file | no_action",
      "source": "optional",
      "destination": "optional",
      "reason": "why this action is needed"
    }}
  ]
}}
"""

        # Send prompt to Gemini
        response = self.model.generate_content(prompt)

        # Gemini sometimes wraps JSON in text — we must be careful
        raw_text = response.text.strip()

        try:
            # Parse the JSON safely
            plan = json.loads(raw_text)
        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned invalid JSON. Output was:\n" + raw_text
            )

        return plan
