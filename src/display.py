import matplotlib.pyplot as plt
import numpy as np
import math

def ObservedOrder(h:list,f:list)->float:
    """create a plot for the order of convergence from the result of 3 meshs

    Args:
        h (float): meshes sizes
        f (list): result value. e.g. the lift coefficient

    Returns:
        list: [description]
    """    
    h = np.array(h)
    f = np.array(f)

    x = np.log(h)
    y = np.log(f)

    x1, x0 = np.polyfit(x,y,1)



    plt.figure()

    plt.xlabel("ln(h)")
    plt.ylabel("ln(CL)")

    plt.scatter(x,y)
    plt.plot(x,x0+x*x1)
    plt.show()

    return x1

def SRQ(h:list, f:list)->float:
    p_hat = math.log((f[1]-f[0])/(f[2]-f[1]))/math.log(2)
    return p_hat
