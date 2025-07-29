from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .tsal_executor import TSALExecutor, TSALOp

class ProgramStack:
    """Simple LIFO stack for execution state."""

    def __init__(self) -> None:
        self._data: List[Any] = []

    def push(self, value: Any) -> None:
        self._data.append(value)

    def pop(self) -> Any:
        return self._data.pop()

@dataclass
class SymbolicFrame:
    """Represents a call or loop boundary."""

    return_ip: int
    stack_start: int

@dataclass
class OpcodeInstruction:
    opcode: TSALOp
    args: Dict[str, Any] = field(default_factory=dict)

class FlowRouter:
    """Executes OpcodeInstructions using TSALExecutor."""

    def __init__(self, executor: TSALExecutor | None = None) -> None:
        self.executor = executor or TSALExecutor()
        self.stack = ProgramStack()
        self.frames: List[SymbolicFrame] = []

    def run(self, program: List[OpcodeInstruction]) -> TSALExecutor:
        seq = [(inst.opcode, inst.args) for inst in program]
        self.executor.execute(seq, mode="EXECUTE")
        return self.executor

def tsal_run(opcodes: List[int]) -> TSALExecutor:
    """Helper for running raw opcode lists."""
    program = [OpcodeInstruction(TSALOp(op)) for op in opcodes]
    router = FlowRouter()
    return router.run(program)
