from os import sep, write
from InputParam import InputParam
from pathlib import Path
from typing import Union
import math
from datetime import datetime

def ControlFileWriter(inputParam: InputParam, outPath: Union[str,Path]):
    outPath = Path(outPath)
    with outPath.open("w") as file:
        # Header
        file.write(CreateSeparator())
        file.write(CreateSeparator("EES2D Software Input File", r"%"))
        file.write("This file was generated using the automated ControlFileWriter\n")
        
        now = datetime.now()
        file.write("Date : " + now.strftime("%d/%m/%Y %H:%M:%S\n"))
        file.write(CreateSeparator())
        file.write("\n")
        file.write("START\n")
        file.write("\n")

        # Pre-processing control
        file.write(CreateSeparator("PRE-PROCESSING CONTROL"))
        file.write("# Extension of the mesh file . Options : SU2 | GMSH (Not implemented yet)")
        file.write("MESH_FORMAT = " + inputParam.meshFormat + "\n\n")
        file.write("# Path to mesh file (from executable directory)\n")
        file.write("MESH_FILE = " + str(inputParam.meshFile) + "\n\n")
        file.write("# Type of mesh. Options : STRUCTURED | UNSTRUCTURED\n")
        file.write("MESH_TYPE = " + inputParam.meshType + "\n\n")

        # Simulation control
        file.write(CreateSeparator("SIMULATION CONTROL"))
        file.write("# Type of speed. Unchosen field will be ignored. Options : MACH | VELOCITY\n")
        file.write("SPEED_OPTION = " + inputParam.spdOpt + "\n\n")

        file.write("# Velocity in m/s\n")
        file.write("VELOCITY = " + str(inputParam.velocity) + "\n\n")

        file.write("MACH = " + str(inputParam.mach) + "\n\n")

        file.write("# Angle of attack in degrees\n")
        file.write("AOA = " + str(inputParam.aoa) + "\n\n")

        file.write("# Airflow pressure in Pa\n")
        file.write("AIRFLOW_PRESSURE = " + str(inputParam.pressure) + "\n\n")

        file.write("# Temperature in K\n")
        file.write("AIRFLOW_TEMPERATURE = " + str(inputParam.temp) + "\n\n")

        file.write("# Viscosity in Ns/m^2\n")
        file.write("AIRFLOW_VISCOSITY = " + str(inputParam.viscosity) + "\n\n")

        file.write("# Density in kg/m^3\n")
        file.write("AIRFLOW_DENSITY = " + str(inputParam.rho) + "\n\n")

        file.write("# Gamma value\n")
        file.write("GAMMA = " + str(inputParam.gamma) + "\n\n")

        file.write("# Gas constant in J/kg.K\n")
        file.write("GAS_CONSTANT = " + str(inputParam.gasConstant) + "\n\n")

        file.write("# Specific heat in J/Kg.k\n")
        file.write("SPECIFIC_HEAT = " + str(inputParam.specificHeat) + "\n\n")

        # Solver Control
        file.write(CreateSeparator("SOLVER CONTROL"))

        file.write("# Discretization of the Convective Fluxes . Options : ROE | AUSM (not implement yet)\n")
        file.write("SCHEME = " + inputParam.scheme + "\n\n")

        file.write("# Minimum residual to stop solver\n")
        file.write("MIN_RESIDUAL = " + str(inputParam.minimumResidual) + "\n\n")

        file.write("# Number of maximum iterations to stop solver\n")
        file.write("MAX_ITER = " + str(inputParam.maxIteration) + "\n\n")

        file.write("# Number of opemmp threads used by the solver\n")
        file.write("OPENMP_THREAD_NUM = " + str(inputParam.openMPThreads) + "\n\n")

        # Post-processing control
        file.write(CreateSeparator("POST-PROCESSING CONTROL"))

        file.write("# Post processng file format . Options : TECPLOT | VTK\n")
        file.write("OUTPUT_FORMAT = " + inputParam.outputFormat + "\n\n")

        file.write("# Path to file output, from executable directory\n")
        file.write("OUTPUT_FILE = " + str(inputParam.outputPath) + "\n\n")

        file.write("# generate log file . Options : TRUE | FALSE\n")        
        file.write("GENERATE_LOG = " + str(inputParam.isLogGenerated).upper() + "\n\n")

        # END

        file.write("\n\nEND")

def CreateSeparator(title: str="", symbol: str="-", length: int=80) -> str:
    """Formats a visual line separator

    Args:
        title (str, optional): string to be inserted in the middle of the separator. Defaults to "".
        symbol (str, optional): symbol to use as a separator. Defaults to "-".
        length (int, optional): total number of characters in the separator. Defaults to 80.

    Raises:
        ValueError: length must be >= to the length of title +2 

    Returns:
        str: separator string
    """    
    if title == "":
        newTitle = title
    else:
        newTitle = " " + title + " "

    nbSym = length-len(newTitle)
    if nbSym <0:
        raise ValueError("title value: %s is longer then the separator length of %i"%(title,length))
    
    separator = symbol*math.floor(nbSym/2) + newTitle + symbol*math.ceil(nbSym/2) + "\n"

    return separator 

if __name__ == "__main__":
    ControlFileWriter(InputParam("this/is/a/mesh.su2"),"controlFile.ees2d")