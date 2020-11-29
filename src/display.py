import matplotlib.pyplot as plt
import numpy as np
import math

def Vassbergfig39(NC: list, Cl: list, savePath: str = "Vassbergfig39.png"):
    """Recreate the plot from Vassberg and Jameson fig39 and overlay custom data points

    Args:
        NC (list): mesh sizes to be overlayed
        Cl (list): Corresponding Cl values
    """
    # Data taken from : Table 8  CFL3D-flux-splitting transonic data at M 0.8
    # alpha = 1.25      no vortex-correction
    NC_V         = np.array([256.         , 512.         , 1024.         , 2048          ])
    Cl_V_125     = np.array([  0.359073197,   0.357580694,    0.355943711,    0.354593186])
    Cl_V_star    = 0.348226045

    p_V          = 0.278

    NC = np.array(NC)
    Cl = np.array(Cl)
    
    # ------------------------ Plotting ---------------------------------
    plt.figure()
    
    # Vassberg points
    x_V = np.log10(np.power(NC_V,-1))
    y_V = np.log10(abs(Cl_V_125-Cl_V_star))
    plt.scatter(x_V,y_V,label="Vassberg et Jameson")

    # Vassberg convergence line
    x_O_V = np.array([min(x_V),-1])
    y_O_V = x_O_V*p_V

    b = min(y_O_V)-min(y_V)

    plt.plot(x_O_V,y_O_V-b,"--")

    # your data
    x = np.log10(np.power(NC,-1))
    y = np.log10(np.abs(Cl-Cl_V_star))
    plt.scatter(x,y, label="Code PI4")


    # 
    plt.xlabel("Log(1/NC)")
    plt.ylabel("Log( abs(Cl-Cl*) )")

    plt.xlim([-4,-1])
    plt.ylim([-5, 0])
    
    plt.grid(True, "major")
    
    plt.legend()
    plt.savefig(savePath)

if __name__ == "__main__":
    Vassbergfig39([17., 33. ,65. ],[0.135716, 0.192864, 0.256218])