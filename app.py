"""
app.py

This file provides a Streamlit-based UI for ActiFlow AI.

Responsibilities:
- Collect user input
- Display results
- Call the AgentController

IMPORTANT:
- This file contains NO business logic
- It only interacts with the controller
"""

import os
import streamlit as st

from agent.controller import AgentController
from tools.utils import normalize_path



def get_system_state(base_directory: str):
    """
    Create a snapshot of the current system state.

    This function:
    - Lists files and folders
    - Does NOT modify anything
    - Provides context to the AI planner
    """
    state = {"files": [], "folders": []}

    for root, dirs, files in os.walk(base_directory):
        for d in dirs:
            state["folders"].append(os.path.join(root, d))
        for f in files:
            state["files"].append(os.path.join(root, f))

    return state


# -------------------------------
# Streamlit UI starts here
# -------------------------------

st.set_page_config(
    page_title="ActiFlow AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 ActiFlow AI")
st.subheader("A Responsible AI Agent That Plans, Acts, and Explains")

st.markdown(
    """
This tool demonstrates an **AI agent** that:
- Plans actions using AI
- Validates them for safety
- Executes them responsibly

⚠️ Actions are restricted to the selected directory.
"""
)

# User input: base directory
base_directory = st.text_input(
    "📂 Base Directory (allowed workspace)",
    value="data/sample_files"
)
base_directory = normalize_path(base_directory)


# User input: task description
user_task = st.text_area(
    "📝 What do you want the agent to do?",
    placeholder="Example: Organize all PDF files into folders by topic"
)

# Run button
run_button = st.button("🚀 Run Agent")

if run_button:
    # Basic input validation
    if not base_directory or not os.path.exists(base_directory):
        st.error("❌ Base directory does not exist.")
    elif not user_task.strip():
        st.error("❌ Please enter a task for the agent.")
    else:
        try:
            # Show progress to the user
            with st.spinner("🤖 Agent is planning and executing..."):
                # Create system state snapshot
                system_state = get_system_state(base_directory)

                # Initialize controller
                controller = AgentController(base_directory)

                # Run the agent
                result = controller.run(
                    user_task=user_task,
                    system_state=system_state
                )

            # Display results
            st.success("✅ Agent completed successfully!")

            st.subheader("🧠 Plan Summary")
            st.write(result["plan_summary"])

            st.subheader("⚙️ Actions Executed")
            for action in result["actions_executed"]:
                st.markdown(
                    f"""
- **Action:** {action['action']}
- **Source:** {action.get('source')}
- **Destination:** {action.get('destination')}
- **Reason:** {action['reason']}
"""
                )

        except Exception as e:
            st.error(f"❌ Agent execution failed: {str(e)}")
