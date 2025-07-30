from __future__ import annotations

import base64
import pickle
from typing import Mapping, Optional

import numpy as np
from pyquil.api._abstract_compiler import QuantumExecutable
from pyquil.api._qam import QAMExecutionResult


class StrangeworksExecutionResult(QAMExecutionResult):
    def __init__(
        self,
        executable: QuantumExecutable = None,
        readout_data: Mapping[str, Optional[np.ndarray]] = None,
        strangeworks_process_time: int = None,
        compilation_time: int = None,
        execution_time: int = None,
        native_quil_to_executable_time: int = None,
        quil_compile_time: int = None,
    ):
        self.executable = executable
        # self.readout_data = readout_data
        self.strangeworks_process_time = strangeworks_process_time
        self.compilation_time = compilation_time
        self.execution_time = execution_time
        self.native_quil_to_executable_time = native_quil_to_executable_time
        self.quil_compile_time = quil_compile_time

    @classmethod
    def from_json(cls, payload: dict) -> StrangeworksExecutionResult:
        # pickled_res = payload["pickled_result"]
        # pickle_bytes = base64.b64decode(pickled_res)
        # qer = pickle.loads(pickle_bytes)
        # TOM: HERE you will probably need to adapt to pyquil4
        print("from_json!!!!")
        return StrangeworksExecutionResult(
            executable=None,  # qer.executable,
            readout_data=None,  # qer.readout_data,
            strangeworks_process_time=payload["strangeworks_process_time"],
            compilation_time=payload["compilation_time"],
            execution_time=payload["execution_time"],
            native_quil_to_executable_time=payload["native_quil_to_executable_time"],
            quil_compile_time=payload["quil_compile_time"],
        )
