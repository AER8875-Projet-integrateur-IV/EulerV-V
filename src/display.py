import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

# -------------------------------------------------------------------------------
# export PGF for latex 
# comment if you want to output a .png
# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
# })
# -------------------------------------------------------------------------------

def Vassbergfig39(NC: list, Cl: list, savePath: str = "Vassbergfig39.pgf", mach = 0.8):
    """Recreate the plot from Vassberg and Jameson fig39 and overlay custom data points

    Args:
        NC (list): mesh sizes to be overlayed
        Cl (list): Corresponding Cl values
    """

    if mach == 0.8:
        # Data taken from : Table 8  CFL3D-flux-splitting transonic data at M 0.8
        # alpha = 1.25      no vortex-correction
        NC_V         = np.array([256.         , 512.         , 1024.         , 2048          ])
        Cl_V_125     = np.array([  0.359073197,   0.357580694,    0.355943711,    0.354593186])
        Cl_V_star    = 0.348226045

        p_V          = 0.278
    elif mach == 0.5:
        # Data taken from : Table 7  CFL3D-flux-splitting transonic data at M 0.5
        # alpha = 1.25      no vortex-correction
        NC_V         = np.array([256.         , 512.         , 1024.         , 2048          ])
        Cl_V_125     = np.array([  0.178366720,   0.179125033,    0.179487608,    0.179650543])
        Cl_V_star    = 0.179783519

        p_V          = 1.154
    else:
        raise NotImplementedError

    NC = np.array(NC)
    Cl = np.array(Cl)
    # ------------------------ Plotting ---------------------------------
    plt.figure(figsize=(6,3))
    
    # Vassberg points
    x_V = np.log10(np.power(NC_V,-1))
    y_V = np.log10(abs(Cl_V_125-Cl_V_star))
    plt.scatter(x_V,y_V,label="Vassberg et Jameson, O(0.278), Cl*=%.5f"%Cl_V_star)

    # Vassberg convergence line
    x_O_V = np.array([min(x_V),-1])
    y_O_V = x_O_V*p_V

    b = min(y_O_V)-min(y_V)

    plt.plot(x_O_V,y_O_V-b,"--")
    plt.subplots_adjust(bottom=0.14,left=0.14)
    
    # your data
    Cl_calcul = Cl
    Cl_star = Cl_calcul[-1]+(Cl_calcul[-1]-Cl_calcul[-2])/(2**1-1)
    h = np.power(NC,-1)
    error = np.abs(Cl-Cl_star)
    x = np.log10(h)
    y = np.log10(error)
    p_hat = math.log((Cl_calcul[-2]-Cl_calcul[-3])/(Cl_calcul[-1]-Cl_calcul[-2]))/math.log(2)
    print("Cl*=%f | Cl p=%f"%(Cl_star,p_hat))
    plt.scatter(x,y, label="Code PI4, O(%.3f), Cl*=%.5f"%(p_hat,Cl_star))


    # 
    plt.xlabel("Log(1/NC)")
    plt.ylabel("Log( abs(Cl-Cl*) )")
    # plt.title("Cl* = %.9f"%Cl_V_star,loc="left",fontdict={'size':10})

    plt.xlim([-4,-1])
    plt.ylim([-5, 0])
    
    plt.grid(True, "major")

    plt.legend(loc="lower right")
    plt.show()
    plt.savefig(savePath)
    # plt.savefig(savePath)
    plt.close()

def PressureCurves(x,p, savePath: str = "PressurCurves.pgf"):
    # ------------------------ Plotting ---------------------------------
    plt.figure(figsize=(4,2))
    plt.subplots_adjust(bottom=0.14,left=0.15)

    # your data
    plt.scatter(x,p,s=1, label="Code PI4")

    plt.xlim([- .2,1.2])
    plt.ylim([-1.2,1.2])

    plt.xlabel("x/c")
    plt.ylabel("Cp",labelpad=-7)
    plt.gca().invert_yaxis()    

    # plt.legend()
    plt.show()

    plt.savefig("test.svg", format="svg")


    # plt.savefig(savePath)
    plt.close()

def Residu(resPath, lastIt=-1):
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

if __name__ == "__main__":
    # This code will run if you execute this module with the following command
    # $ python display.py

    file = r"livrableA/analyseMach08.dat"
    data = np.loadtxt(file, skiprows=1)
    NC = data[:-1,0]
    Cl = data[:-1,1]
    Vassbergfig39(NC,Cl,"p08.png",mach=0.8)

    # # Cd order and continuum
    # Cd = data[:-1,2]
    # Cd_star = Cd[-1]+(Cd[-1]-Cd[-2])/(2**1-1)
    # error = np.abs(Cd-Cd_star)
    # y = np.log10(error)
    # p_hat = np.log10((Cd[-2]-Cd[-3])/(Cd[-1]-Cd[-2]))/np.log10(2)
    # print("Cd*=%f | Cd p=%f"%(Cd_star,p_hat))

    # Read pressure file
    # file = r"analyseRef05_512/pressure.dat"
    # data = np.loadtxt(file,skiprows=4)
    # x = data[:,0]
    # p = data[:,1]
    # PressureCurves(x,p)