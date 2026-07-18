from dataclasses import dataclass, field


@dataclass
class ExecutionStep:
    tool: str | None
    parameters: dict = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    steps: list[ExecutionStep] = field(default_factory=list)