
from os import name
import EESwrapper.wrapper as wrapper
import EESwrapper.InputParam as InputParam
from pathlib import Path
import constants
import numpy as np
import matplotlib.pyplot as plt
import math

def SolveCL(filepath,mesh,size):
    """Run the simulation on multiples AOA and write resulting CL and CD to a file

    Returns:
        [type]: [description]
    """    
    # Wrapper initialisation
    EES2D = wrapper.wrapper(constants.EXEC_EES2D_APP)

    # mach number from Reynolds definition
    Re = 1e7
    c = 1
    mu = 1.853e-05
    rho = 1.2886
    velocity = Re*mu/c/rho      # m/s

    gamma = 1.4
    T = 288.15
    R = 287.058

    c = math.sqrt(gamma*R*T)

    mach = velocity/c

    # starting simulations
    CL_ar = []
    CD_ar = []
    time_ar = []
    lastRes_ar = []

    with open(filepath, "a") as file:
        file.write("{:<20}".format("alpha")         + 
                   "{:<20}".format("CL")            + 
                   "{:<20}".format("CD")            + 
                   "{:<20}".format("time (s)")      + 
                   "{:<20}".format("Res. RMS fin")  +
                   "\n")

    alpha_ar =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    for i, alpha in enumerate(alpha_ar):
        input = InputParam.InputParam(meshFile=mesh,aoa=alpha,maxIteration=int(1e5), minimumResidual=1e-15,cfl=6,timeIntegration=InputParam.SCHEME_TIME_RK5,
                                      viscosity=mu,rho=rho,gamma=gamma,gasConstant=R,temp=T,mach=mach,logPath="log%i.txt"%size,residualPath="residuals%i.dat"%size)

        sim = EES2D.RunSim(input,additionalArgs=[])

        outputfolder = Path(".")/"analyseValidation_{:.0f}_{:.0f}".format(size,alpha)
        sim.move2folder(outputfolder)
        
        CL, CD = sim.getCoefficients()

        residuals = sim.GetResiduals()
        lastRes_ar.append(np.max(residuals[-1,:]))

        CL_ar.append(CL)
        CD_ar.append(CD)
        time_ar.append(sim.time)

        result_str = "{:<15.0f}     {:<15.6f}     {:<15.6f}     {:<15.6f}     {:<15.6e}".format(alpha,CL_ar[i],CD_ar[i],time_ar[i],lastRes_ar[i]) + "\n"
        with open(filepath, "a") as file:
            file.write(result_str)

def getGCI(f1,f2,f3):
    r=2
    try:
        p_hat = math.log((f3-f2)/(f2-f1))/math.log(r)
    # x=np.log(np.power(np.array([128.,256.,512.]),-1))
    # star = 
    # y=np.log(np.array([f3,f2,f1]))
    # p_hat = np.polyfit(x,y,1)[0]
    except:
        return 0, -1
    pf =1
    error = (p_hat-pf)/pf
    if error <=0.1:
        Fs = 1.25
        p = pf
    elif error>0.1:
        Fs = 3
        p = min(max(0.5,p_hat),pf)
    else:
        raise NotImplementedError
    GCI = Fs/(r**p-1)*abs(f3-f2)
    return GCI, p_hat

def solveComputationalError():
    alpha_ar = np.linspace(0,11,12)

    # extract data
    data_128 = np.loadtxt("validation/NC128/testValidation.dat", skiprows=1)
    data_256 = np.loadtxt("validation/NC256/testValidation.dat", skiprows=1)
    data_512 = np.loadtxt("validation/NC512/testValidation.dat", skiprows=1)

    # solve GCI
    GCI = np.zeros((2,len(alpha_ar)))
    p_hat = np.zeros((2,len(alpha_ar)))
    for alpha in range(len(alpha_ar)):
        f1_ar = data_512[alpha,1:3]
        f2_ar = data_256[alpha,1:3]
        f3_ar = data_128[alpha,1:3]

        for coef in range(2):
            f1 = f1_ar[coef]
            f2 = f2_ar[coef]
            f3 = f3_ar[coef]
            GCI[coef,alpha], p_hat[coef,alpha] = getGCI(f1,f2,f3)

    # write to file
    with open("modelError.dat","w") as file:
        file.write("{:<20}".format("alpha")            + 
                   "{:<20}".format("GCI Cl")           + 
                   "{:<20}".format("p_hat Cl")         + 
                   "{:<20}".format("GCI Cd")           + 
                   "{:<20}".format("p_hat Cd")         + 
                   "\n")
        for i, alpha in enumerate(alpha_ar):
            file.write("{:<15.9f}     ".format(alpha)         + 
                       "{:<15.9f}     ".format(GCI[0,i])        + 
                       "{:<15.9f}     ".format(p_hat[0,i])      + 
                       "{:<15.9f}     ".format(GCI[1,i])        + 
                       "{:<15.9f}     ".format(p_hat[1,i])      + 
                       "\n")

def PlotValidation():
    pass

if __name__=="__main__":
    # solveComputationalError()
    SolveCL("testValidation128.dat",constants.MESH_EULER_129x129,128)
    SolveCL("testValidation128.dat",constants.MESH_EULER_256x256,256)
