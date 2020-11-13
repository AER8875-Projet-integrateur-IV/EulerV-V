from InputParam import InputParam
from pathlib import Path
from typing import Union

class sim():
    def __init__(self, controlPath: Union[str, Path], inputParam: InputParam) -> None:
        self.inputParam = inputParam
        self.logPath = inputParam.logPath
        self.residualPath = inputParam.residualPath
        self.pressurePath = inputParam.pressurePath
        self.controlPath = controlPath

            