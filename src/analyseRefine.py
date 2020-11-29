"""
Module containing the functions needed for a refinment study
"""

from os import name
import EESwrapper.wrapper as wrapper
import EESwrapper.InputParam as InputParam
from pathlib import Path
import constants
import numpy as np
import matplotlib.pyplot as plt


def SolveCL():
    """Run the simulation on multiples meshes and write resulting CL and CD to a file

    Returns:
        [type]: [description]
    """    
    # Wrapper initialisation
    EES2D = wrapper.wrapper(constants.EXEC_EULER2D_A)
    meshes = [constants.MESH_EULER_17x17,
              constants.MESH_EULER_17x17,
              constants.MESH_EULER_33x33,
              constants.MESH_EULER_65x65,
              constants.MESH_EULER_129x129,
              constants.MESH_EULER_256x256,
              constants.MESH_EULER_513x513]
    size = np.array([9.,17.,33.,65.,129.,256.,513.])

    CL_ar = []
    CD_ar = []

    for i, mesh in enumerate(meshes):
        input = InputParam.InputParam(meshFile=mesh,aoa=1.25,mach=0.5,maxIteration=int(1e6), minimumResidual=1e-6)

        sim = EES2D.RunSim(input,additionalArgs=["-vv"])

        outputfolder = Path(".")/"analyseRefSub{:.0f}".format(size[i])
        sim.move2folder(outputfolder)
        
        CL, CD = sim.getCoefficients()

        print(CL, CD)

        CL_ar.append(CL)
        CD_ar.append(CD)

    # print results
    result_str = "------------- Results -----------------\n"
    result_str += "{:<15}".format("size") + "{:<15}".format("CL") + "{:<15}".format("CD") +"\n"
    for i in range(len(meshes)):
        result_str += "{:<10.0f}     {:<10.6f}     {:<10.6f}".format(size[i],CL_ar[i],CD_ar[i]) + "\n"
    print(result_str)

    path = "analyseRefSub.txt"
    with open(path, "w") as file:
        file.write(result_str)

    return path

def Plot(path):
    # ReadData
    data = np.loadtxt(path,skiprows=2)
    print(data)
    n  = np.array([data[i,0] for i in range(data.shape[0])])
    CL = np.array([data[i,1] for i in range(data.shape[0])])
    CD = np.array([data[i,2] for i in range(data.shape[0])])

    r = 2
    p = 1
    CL_rich = CL[-1]+(CL[-1]-CL[-2])/(2**1-1)
    CD_rich = CD[-1]+(CD[-1]-CD[-2])/(2**1-1)

    richardson = (CL_rich,CD_rich)
    name = ("CL","CD")
    for i, studied_coeff in enumerate([CL,CD]): 
        # find convergence rate
        print(richardson[i])
        print(studied_coeff[2:])
        y = np.log(abs(studied_coeff[2:]-richardson[i]))
        print(y)
        x = np.log(np.power(n[2:],-1))
        x1, x0 = np.polyfit(x, y, 1)    

        # Convergence plot
        plt.figure()

        plt.plot(x,x0+x1*x,"--",label="%s = %f+%f*ln(h)"%(name[i],x0,x1))
        plt.scatter(x,y,label=name[i])

        plt.xlabel("ln(h)")
        plt.ylabel(r"ln(erreur)")

        plt.legend()
        plt.savefig("OrdreConv%s.png"%name[i])
        plt.close()

        # Regular plot
        plt.figure()

        plt.scatter(n,studied_coeff)

        plt.xlabel("n")
        plt.ylabel("%s"%name[i])

        plt.legend()
        plt.savefig("%s.png"%name[i])
        plt.close()

if __name__ == "__main__":
    # SolveCL()
    Plot(r"/mnt/linuxHDD/PI4/EulerV-V/analyseRefSub/analyseRefSub.txt")