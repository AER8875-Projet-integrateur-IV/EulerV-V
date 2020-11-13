from dataclasses import dataclass
from typing import Union
from pathlib import Path

# Mesh formats
MESH_FORMAT_SU2 = "su2"

# Mesh types
MESH_TYPE_UNSTRUCT = "unstructured"
MESH_TYPE_STRUCT = "structured"

# Speed options
SPD_OPTION_MACH = "MACH"
SPD_OPTION_VELOCITY = "VELOCITY"

# schemes
SCHEME_ROE = "ROE"
SCHEME_AVERAGE = "AVERAGE"
SCHEME_AUSM = "AUSM"

# output formats
OUTPUT_FORMAT_TECPLOT = "Tecplot"
OUTPUT_FORMAT_VTU = "VTU"

@dataclass
class InputParam():
    # ---------------- necessary inputs ---------------- 
    
    # Mesh options
    meshFile: Union[str,Path]
    
    # ---------------- optional inputs ----------------- 

    # Mesh options
    meshFormat: str = MESH_FORMAT_SU2
    meshType: str = MESH_TYPE_UNSTRUCT

    # Simulation control
    spdOpt: str = SPD_OPTION_MACH
    velocity: float = 0
    mach: float = 2.5
    aoa: float = 0
    pressure: float= 101325
    temp: float= 288.15
    viscosity: float= 1.853e-5
    rho: float= 1.2886
    gamma: float= 1.4
    gasConstant: float = 287.058
    specificHeat: float = 1004.7

    # solver control
    scheme: str = SCHEME_ROE
    minimumResidual:float = 1e-8
    maxIteration: int = 200
    openMPThreads: int = 4

    # Post-processor control
    outputFormat: str = OUTPUT_FORMAT_TECPLOT
    isLogGenerated: bool = True
    outputPath: Union[str,Path] = Path("output.dat")
    logPath: Union[str,Path] = Path("log.txt")
    residualPath: Union[str,Path] = Path("residuals.dat")
    pressurePath: Union[str,Path] = Path("pressure.dat")
