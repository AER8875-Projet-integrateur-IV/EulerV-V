import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

# -------------------------------------------------------------------------------
# export PGF for latex 
# comment if you want to output a .png
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
# -------------------------------------------------------------------------------

def Vassbergfig39(NC: list, Cl: list, savePath: str = "Vassbergfig39.pgf"):
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
    plt.figure(figsize=(4,3))
    
    # Vassberg points
    x_V = np.log10(np.power(NC_V,-1))
    y_V = np.log10(abs(Cl_V_125-Cl_V_star))
    plt.scatter(x_V,y_V,label="Vassberg et Jameson, O(0.278)")

    # Vassberg convergence line
    x_O_V = np.array([min(x_V),-1])
    y_O_V = x_O_V*p_V

    b = min(y_O_V)-min(y_V)

    plt.plot(x_O_V,y_O_V-b,"--")
    plt.subplots_adjust(bottom=0.14,left=0.14)
    
    # your data
    h = np.power(NC,-1)
    error = np.abs(Cl-Cl_V_star)
    x = np.log10(h)
    y = np.log10(error)
    p_hat = (y[-1]-[-2])/np.log(2)
    plt.scatter(x,y, label="Code PI4            , O(%.3f)"%p_hat)


    # 
    plt.xlabel("Log(1/NC)")
    plt.ylabel("Log( abs(Cl-Cl*) )")
    plt.title("Cl* = %.9f"%Cl_V_star,loc="left",fontdict={'size':10})

    plt.xlim([-4,-1])
    plt.ylim([-5, 0])
    
    plt.grid(True, "major")

    plt.legend()
    plt.show()
    plt.savefig(savePath)
    plt.close()

def PressureCurves(x,p, savePath: str = "PressurCurves.pgf"):
    # ------------------------ Plotting ---------------------------------
    plt.figure(figsize=(3.2,3.2))
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

    plt.savefig(savePath)
    plt.close()

if __name__ == "__main__":
    # This code will run if you execute this module with the following command
    # $ python display.py

    file = r"analyseMach08.dat"
    data = np.loadtxt(file, skiprows=1)
    NC = data[:,0]
    Cl = data[:,1]
    Vassbergfig39(NC,Cl)

    # Read pressure file
    file = r"analyseRef08_512/pressure.dat"
    data = np.loadtxt(file,skiprows=4)
    x = data[:,0]
    p = data[:,1]
    PressureCurves(x,p)