from InputParam import InputParam
from pathlib import Path
from typing import Union, Optional
import subprocess
import ControlFileWriter
from datetime import datetime

class wrapper:
    def __init__(self, executable: str) -> None:
        self.executable = executable

    def RunSim(self, inputParam: InputParam, controlPath: Optional[Union[str,Path]] = None, additionalArgs: Optional[list] = None):
        if controlPath == None:
            now = datetime.now()
            controlPath = Path(now.strftime("commandFile%H_%M_%S.ees2d"))
        else:
            controlPath = Path(controlPath)

        # write control file
        ControlFileWriter.ControlFileWriter(inputParam,controlPath)

        self._Send2Terminal(controlPath, additionalArgs)


    def _Send2Terminal(self,controlPath: Union[str,Path],additionalArgs: Optional[list] = None) -> None:
        command = [self.executable, str(controlPath)]
        if additionalArgs != None:
            command.extend(additionalArgs)
        subprocess.run(command)

