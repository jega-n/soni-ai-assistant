import json

from assistant.brain.execution_plan import ExecutionPlan, ExecutionStep
from assistant.brain.prompts import PLANNER_PROMPT


class LLMPlanner:

    def __init__(self, llm, registry):
        self.llm = llm
        self.registry = registry

    def plan(self, user_message: str):

        available_tools = json.dumps(
            self.registry.planner_tools(),
            indent=2
        )

        prompt = f"""
{PLANNER_PROMPT}

Available Tools:

{available_tools}

User Request:
{user_message}
"""

        response = self.llm.generate(prompt)

        try:

            start = response.find("{")
            end = response.rfind("}") + 1

            if start == -1 or end == 0:
                raise ValueError("No JSON found.")

            data = json.loads(response[start:end])

            steps = []

            for step in data.get("steps", []):

                steps.append(
                    ExecutionStep(
                        tool=step.get("tool"),
                        parameters=step.get("parameters", {})
                    )
                )

            return ExecutionPlan(steps=steps)

        except Exception:

            return ExecutionPlan()