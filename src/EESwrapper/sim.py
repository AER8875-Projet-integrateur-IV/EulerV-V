from logging import raiseExceptions
from os import name
from EESwrapper.InputParam import InputParam
from pathlib import Path, PurePath
from typing import Tuple, Union, Optional
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
import re
import tecplot.data
from collections import namedtuple
import copy

@dataclass
class sim_path():
    log: Path
    residual: Path 
    pressure: Path 
    control: Path 
    output: Path 
    mms :Path

    def __iter__(self):
        iterable = (self.log, self.residual, self.pressure, self.control, self.output, self.mms)
        return iterable.__iter__()

    def delete(self):
        for file in self:
            file.unlink(missing_ok=True)

    def move2folder(self, path):
        path = Path(path)
        # create dir
        while True:
            try:
                path.mkdir()
                break
            except FileExistsError:                
                path = path.parent/(path.stem+"copy"+path.suffix)
                

        # move files
        try:
            self.log = self.log.replace(path/self.log.name)
        except:
            pass
        try:
            self.residual = self.residual.replace(path/self.residual.name)
        except:
            pass
        try:
            self.pressure = self.pressure.replace(path/self.pressure.name)
        except:
            pass
        try:
            self.control = self.control.replace(path/self.control.name)
        except:
            pass
        try:
            self.output = self.output.replace(path/self.output.name)
        except:
            pass
        try:
            self.mms = self.mms.replace(path/self.mms.name)
        except:
            pass


class sim():
    """Represents a simulation, can be used to acces the different outputs through python
    """    
    def __init__(self, controlPath: Union[str, Path], inputParam: InputParam) -> None:
        self.inputParam = inputParam
        self.paths = sim_path(Path(inputParam.logPath),
                              Path(inputParam.residualPath),
                              Path(inputParam.pressurePath),
                              Path(controlPath),
                              Path(inputParam.outputPath),
                              Path("MMSoutput.dat"))
        self.time = 0 
        
    def GetResiduals(self)->np.ndarray:
        array = np.loadtxt(str(self.paths.residual),skiprows=6)
        # array = np.loadtext(str(self.residualPath),skiprows=5)
        return array

    def deleteFiles(self):
        """Delete all output files relating to this simulation
        """        
        self.paths.delete()

    def plotResiduals(self, savePath: Optional[Union[str, Path]]=None):
        """PLot the simulation residuals as a function of the iteration number

        Args:
            savePath (Optional[Union[str, Path]], optional): Save path for the resulting fig, the figure will be 
            displayed if no argument is given. Defaults to None.
        """        
        residuals = self.GetResiduals()
        title = "mesh: %s  AOA: %f deg"%(Path(self.inputParam.meshFile).stem, self.inputParam.aoa)

        plt.plot([i for i in range(residuals.shape[0])],residuals[:,0])
        plt.plot([i for i in range(residuals.shape[0])],residuals[:,1])
        plt.plot([i for i in range(residuals.shape[0])],residuals[:,2])
        plt.plot([i for i in range(residuals.shape[0])],residuals[:,3])
        plt.title(title)
        plt.xlabel("Iterations")
        plt.ylabel("residuals")
        plt.legend(["rho_V", "rho_u_V", "rho_v_V","rho_H_V"])
        plt.yscale("log")
        plt.show()
        if savePath != None:
            plt.savefig(savePath)
        else:
            plt.show()
        plt.close()

    def move2folder(self, path: Union[str, Path]):
        """Move all output files relating to this simulation to a new target directory, if a directory
        with the given path allready exists, a new directory will be created with the word "copy" appended

        Args:
            path ([type]): path to the new target directory. Must not already exist
        """        
        self.paths.move2folder(path)

    def getW(self):
        """Extract volume, density, velocity and pressure data from the solution tecplot data file

        Returns:
            namedtuple: tecplotVar named tuple, containing the following attributes: volume, rho, u, v, pressure
        """      
 
        data = tecplot.data.load_tecplot(str(self.paths.output),read_data_option=tecplot.constant.ReadDataOption.Replace)

        tecplotVar = namedtuple("tecplotVar", "volume rho u v pressure")

        vol = data.variable('volume'  ).values(0).as_numpy_array(copy=True)
        rho = data.variable('rho'     ).values(0).as_numpy_array(copy=True)
        u   = data.variable('u'       ).values(0).as_numpy_array(copy=True)
        v   = data.variable('v'       ).values(0).as_numpy_array(copy=True)
        p   = data.variable('pressure').values(0).as_numpy_array(copy=True)

        vars = tecplotVar(vol, rho, u, v, p)

        return vars

    def getMMS(self):
        """Extract volume, density, velocity and pressure data from a tecplot data file

        Returns:
            namedtuple: tecplotVar named tuple, containing the following attributes: rho, u, v, pressure
        """        

        dataMMS = tecplot.data.load_tecplot(str(self.paths.mms),read_data_option=tecplot.constant.ReadDataOption.Replace)

        tecplotVarMMS = namedtuple("tecplotVar", "rho u v pressure")

        rho = dataMMS.variable('rho'     ).values(0).as_numpy_array(copy=True)
        u   = dataMMS.variable('u'       ).values(0).as_numpy_array(copy=True)
        v   = dataMMS.variable('v'       ).values(0).as_numpy_array(copy=True)
        p   = dataMMS.variable('pressure').values(0).as_numpy_array(copy=True)

        vars = tecplotVarMMS(rho, u, v, p)

        return vars

    def getCoefficients(self)->tuple:
        """Read CL from pressure data output file
        """        
        with self.paths.pressure.open("r") as file:
            for i, line in enumerate(file):
                if i == 3:
                    substr = line.split()
                    print(substr)
                    CL = float(substr[2])
                    CD = float(substr[6])
        return CL, CD
                