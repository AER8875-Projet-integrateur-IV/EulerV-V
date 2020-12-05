"""
This module is used as a script for refinement analysis with the method of manufactured solutions 
"""

import EESwrapper.wrapper as wrapper
import EESwrapper.InputParam as InputParam
from pathlib import Path
import constants
import numpy as np
import matplotlib.pyplot as plt

#################################################################################################################
#                                       D E F I N I T I O N S
#################################################################################################################

def solveL2(volumes, ar_1, ar_2) -> float:
    # print(ar_1)
    # print(ar_2)
    L2 = 0
    volume_tot = 0
    for i in range(len(ar_1)):
        volume_tot += volumes[i]
        L2 += volumes[i]*(ar_1[i]-ar_2[i])**2
    L2 = (L2/volume_tot)**0.5
    # print(format(L2, '.60g'))
    return L2

#################################################################################################################
#                                           S C R I P T
#################################################################################################################

def plotMMS(dataPath: str, savePath: str = "MMSfig.png"):
    data = np.loadtxt(dataPath, skiprows=1)
    NC      = np.array(data[2:,0])
    L2_rho  = np.log(np.array(data[2:,1]))
    L2_u    = np.log(np.array(data[2:,2]))
    L2_v    = np.log(np.array(data[2:,3]))
    L2_p    = np.log(np.array(data[2:,4]))

    x =  np.log(np.power(NC,-1))

    # find convergence rates
    x1_rho, x0_rho = np.polyfit(x[-3:], L2_rho[-3:], 1)
    x1_u, x0_u = np.polyfit(x[-3:], L2_u[-3:], 1)
    x1_v, x0_v = np.polyfit(x[-3:], L2_v[-3:], 1)
    x1_p, x0_p = np.polyfit(x[-3:], L2_p[-3:], 1)

    # plot results
    plt.figure()

    plt.scatter(x,L2_rho,label="L2 rho, O(%.3f)"%x1_rho)
    plt.plot(x,x0_rho+x1_rho*x,":")

    plt.scatter(x,L2_u,label="L2 u   , O(%.3f)"%x1_u)
    plt.plot(x,x0_u+x1_u*x,":")

    plt.scatter(x,L2_v,label="L2 v   , O(%.3f)"%x1_v)
    plt.plot(x,x0_v+x1_v*x,":")

    plt.scatter(x,L2_p,label="L2 p   , O(%.3f)"%x1_p)
    plt.plot(x,x0_p+x1_p*x,":")

    plt.plot(x,-0.3+x,"k--",label=("p        , O(1)"))

    plt.xlabel("ln(h)")
    plt.ylabel("ln(L2)")

    plt.legend()
    plt.savefig("EtudeConvergenceMMS.png")    



def Solve():
    EES2D = wrapper.wrapper(constants.EXEC_EULER2D_A_MMS)

    meshes = [constants.MESH_EULER_1025x1025]
    size = np.array([1024.])

    # meshes = [constants.MESH_EULER_1025x1025]
    # size = np.array([1025.])

    L2_rho  = []
    L2_u    = []
    L2_v    = []
    L2_p    = []

    filepath = "EtudeConvergenceMMS.txt"

    result_str = "{:<15}".format("size") + "{:<15}".format("L2_rho") + "{:<15}".format("L2_u") + "{:<15}".format("L2_v") + "{:<15}".format("L2_p") +"\n"
    with open(filepath, "a") as file:
        file.write(result_str)

    for i, mesh in enumerate(meshes):
        input = InputParam.InputParam(meshFile=mesh,aoa=0,mach=1,maxIteration=int(5e6), minimumResidual=1e-13)

        sim = EES2D.RunSim(input,additionalArgs=["-vv","--mms"])

        outputfolder = Path(".")/("MMS%i"%size[i])
        sim.move2folder(outputfolder)
        
        # Get data
        ms  = sim.getMMS()
        sol = sim.getW()

        # Get error 
        L2_rho.append(solveL2(sol.volume, sol.rho     , ms.rho     ))
        L2_u.append(  solveL2(sol.volume, sol.u       , ms.u       ))
        L2_v.append(  solveL2(sol.volume, sol.v       , ms.v       ))
        L2_p.append(  solveL2(sol.volume, sol.pressure, ms.pressure))

        result_str = "{:<10.4e}     {:<10.4e}     {:<10.4e}     {:<10.4e}     {:<10.4e}".format(size[i],L2_rho[i],L2_u[i],L2_v[i],L2_p[i]) + "\n"
        with open(filepath, "a") as file:
            file.write(result_str)

if __name__ == "__main__":
    Solve()
    # plotMMS("EtudeConvergenceMMS.txt")


    # import EESwrapper.sim as simulation
    # input = InputParam.InputParam(meshFile=constants.MESH_EULER_513x513,aoa=0,mach=1,maxIteration=int(5e6), minimumResidual=1e-13)
    # sim = simulation.sim(r"MMS513/commandFile17_00_30.ees2d",input) 
    # sim.updatePaths(outputPath=r"MMS513/output.dat",MMSPath=r"MMS513/MMSoutput512.dat")

    # # Get data
    # ms  = sim.getMMS()
    # sol = sim.getW()

    # # Get error 
    # size=217.
    # L2_rho  =solveL2(sol.volume, sol.rho     , ms.rho     )
    # L2_u    =solveL2(sol.volume, sol.u       , ms.u       )
    # L2_v    =solveL2(sol.volume, sol.v       , ms.v       )
    # L2_p    =solveL2(sol.volume, sol.pressure, ms.pressure)

    # result_str = "{:<10.4e}     {:<10.4e}     {:<10.4e}     {:<10.4e}     {:<10.4e}".format(size,L2_rho,L2_u,L2_v,L2_p) + "\n"
    # with open("EtudeConvergenceMMS.txt", "a") as file:
    #     file.write(result_str)