from EESwrapper.InputParam import InputParam
from pathlib import Path
from typing import Union, Optional
import subprocess
from EESwrapper.ControlFileWriter import ControlFileWriter
from datetime import datetime
import EESwrapper.sim
import time

class wrapper:
    def __init__(self, executable: Union[str,Path]) -> None:
        self.executable = executable

    def RunSim(self, inputParam: InputParam, controlPath: Optional[Union[str,Path]] = None, additionalArgs: Optional[list] = None) -> EESwrapper.sim.sim:
        """Create a control file, runs the simulation and creates a simulation object

        Args:
            inputParam (InputParam): Parameters used to run the simulation
            controlPath ([Union[str,Path]], optional): Path to the control file that will be written. Defaults to None.
            additionalArgs ([list], optional): additionnal arguments to pass when starting the simulation. Defaults to None.

        Returns:
            EESwrapper.sim.sim: [description]
        """        
        if controlPath == None:
            now = datetime.now()
            controlPath = Path(now.strftime("commandFile%H_%M_%S.ees2d"))
        else:
            controlPath = Path(controlPath)

        # write control file
        ControlFileWriter(inputParam,controlPath)

        beg = time.perf_counter()
        self._Send2Terminal(controlPath, additionalArgs)
        end = time.perf_counter()

        # Return object containing sim info
        sim = EESwrapper.sim.sim(controlPath, inputParam)
        sim.time = end-beg
        return sim

    def _Send2Terminal(self,controlPath: Union[str,Path],additionalArgs: Optional[list] = None) -> None:
        """Run a simulation with optional additional arguments

        Args:
            controlPath (Union[str,Path]): Path to the control file
            additionalArgs (Optional[list], optional): List of strings to be supplied as additional arguments for the simulation. Defaults to None.
        """        
        command = [str(self.executable), str(controlPath)]
        if additionalArgs != None:
            command.extend(additionalArgs)
        subprocess.run(command)

