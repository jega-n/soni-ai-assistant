import json
import time
from assistant.brain.execution_plan import ExecutionPlan, ExecutionStep
from assistant.brain.prompts import PLANNER_PROMPT


class LLMPlanner:

    def __init__(self, llm, registry):
        self.llm = llm
        self.registry = registry

    def plan(self, user_message: str):

        start = time.perf_counter()
        available_tools = json.dumps(
            self.registry.planner_tools(),
            indent=2
        )
        print(f"Tool serialization:{time.perf_counter() - start:.2f} seconds")
        print(available_tools)

        msg = [
    {
        "role": "system",
        "content": PLANNER_PROMPT
    },
    {
        "role": "user",
        "content": (
            f"Available Tools:\n\n"
            f"{available_tools}\n\n"
            f"User Request:\n"
            f"{user_message}"
        )
    }
]
        start = time.perf_counter()
        response = self.llm.plan(msg)
        print(f"ollama.chat(plan):{time.perf_counter() - start:.2f} seconds")

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