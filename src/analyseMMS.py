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

if __name__ == "__main__":

    EES2D = wrapper.wrapper(constants.EXEC_EULER2D_A_MMS)

    meshes = [constants.MESH_EULER_9x9,constants.MESH_EULER_17x17,constants.MESH_EULER_33x33,constants.MESH_EULER_65x65,constants.MESH_EULER_129x129,constants.MESH_EULER_256x256]
    size = np.array([9.,17.,33.,65.,129.,256.])

    
    L2_rho  = []
    L2_u    = []
    L2_v    = []
    L2_p    = []

    for i, mesh in enumerate(meshes):
        input = InputParam.InputParam(meshFile=mesh,aoa=0,mach=1,maxIteration=int(1e6), minimumResidual=1e-13)

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


    x =  np.log(np.power(size,-1))
    y = [np.log(L2_rho),
         np.log(L2_u)  ,
         np.log(L2_v)  ,
         np.log(L2_p)  ]

    # find convergence rate
    y_tot = []
    x_tot = []
    for norme in y:
        y_tot.extend(norme)
        x_tot.extend(norme)
    x1, x0 = np.polyfit(x_tot, y_tot, 1)


    # print results
    result_str = "------------- Results -----------------\n"
    result_str += "order= %f\n"%x1
    result_str += "{:<15}".format("size") + "{:<15}".format("L2_rho") + "{:<15}".format("L2_u") + "{:<15}".format("L2_v") + "{:<15}".format("L2_p") +"\n"
    for i in range(len(meshes)):
        result_str += "{:<10.4e}     {:<10.4e}     {:<10.4e}     {:<10.4e}     {:<10.4e}".format(size[i],L2_rho[i],L2_u[i],L2_v[i],L2_p[i]) + "\n"
    print(result_str)

    with open("EtudeConvergenceMMS.txt", "w") as file:
        file.write(result_str)


    # plot results
    plt.figure()
    labels = ("L2 rho", "L2 u", "L2 v", "L2 p")
    for i in range(len(y)):
        plt.scatter(x,y[i],label=labels[i])
    plt.plot(x,x0+x1*x,"-",label="moindre carré")

    plt.xlabel("ln(h)")
    plt.ylabel("ln(L2)")

    plt.legend()
    plt.savefig("EtudeConvergenceMMS.png")
    