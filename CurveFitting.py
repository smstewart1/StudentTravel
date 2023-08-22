#import libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit
import warnings

bin_number = 30

#main function
def main():
    Clist = ["CHM-090.csv", "CHM-130.csv", "CHM-131.csv", "CHM-131A.csv", "CHM-151.csv", "CHM-152.csv", "CHM-251.csv", "CHM-252.csv", "SWC.csv", "SNWC.csv", "PHSC.csv", "RTP.csv"]
    dfList = ["DCHM-090.csv", "DCHM-130.csv", "DCHM-131.csv", "DCHM-131A.csv", "DCHM-151.csv", "DCHM-152.csv", "DCHM-251.csv", "DCHM-252.csv", "DSWC.csv", "DSNWC.csv", "DPHSC.csv", "DRTP.csv"]
    warnings.filterwarnings('ignore')
    
    #builds the running total based on radius
    for i in range(0, len(Clist) - 1):
        df = pd.read_csv(Clist[i])
        dist = np.histogram(df["RadiusHC"], bins = bin_number, density = False)
        tlist = []
        a = 0
        N = dist[0].sum()
        for j in range(0, len(dist[0]) - 1):
            a = a + dist[0][j] / N
            tlist.append([dist[1][j], dist[1][j + 1], a ])
        df_temp = pd.DataFrame(tlist, columns = ["Lower Distance", "Upper Distance", "Percentage of Students"])
        df_temp.to_csv(dfList[i])
        del df
        del df_temp
        del tlist
        del dist
    
    
    curvefits = []
    # gaussian model
    for i in Clist:
        df = pd.read_csv(i)
        dist = df["RadiusHC"]
        mu, sigma = norm.fit(dist)
        plotter_g(dist, i, mu, sigma)
        curvefits.append([i[0:-4], mu, sigma])
        del df
        del dist
    df_temp = pd.DataFrame(curvefits, columns = ["Course", "Mu", "Sigma"])
    df_temp.to_csv("FittingParameters.csv")
    del df_temp    
    
    #log-normal
    custom_fit = []
    for i in Clist:
        df = pd.read_csv(i)
        dist = np.histogram(df["RadiusHC"], bins = bin_number, density = True)
        centers = np.array([0.5 * (dist[1][i] + dist[1][i+1]) for i in range(len(dist[1])-1)])
        popt, pcov = curve_fit(homebrew_g0, xdata = centers, ydata = dist[0])
        x0, s = popt
        custom_fit.append([i[0:-4], x0, s])
        plotter_h(dist, centers, i, x0, s)
        curvefits.append([i[0:-4], popt])
        del df
    df_temp = pd.DataFrame(custom_fit, columns = ["Course", "x0", "s"])
    df_temp.to_csv("CustomFit.csv")
    del df_temp
    
    return    

#additional functions

#log normal distributions
def homebrew_g0(x, x0, s):
    return (1 / (x * s * np.sqrt(2 * 3.141))) * np.exp(-((np.log(x) -x0) ** 2)/(2 * (s ** 2)))


def plotter_h(dist, centers, name, x0, s):
    name = name[0:-4]
    string = f"{name}_g0.png"
    titlest = f"Fraction of Students vs. Miles Traveled for {name}\nLog Normal Distribution"
    
    #plot histrogram
    plt.bar(x = centers, height = dist[0], facecolor = 'green', width = 8)
    
    #plot best fit
    y = homebrew_g0(centers, x0, s)
    l = plt.plot(centers, y, 'r--', linewidth = 2)
    
    #makes the plot readable
    plt.xlabel("Miles Traveled to Campus")
    plt.ylabel("Fraction of Students")
    plt.title(titlest)
    plt.savefig(string)
    plt.clf()
    plt.cla()
    
    return

def plotter_g(data, name, mu, sigma):
    name = name[0:-4]
    string = f"{name}.png"
    titlest = f"Fraction of Students vs. Miles Traveled for {name}\nGaussian Distribution"
    
    #plot histrogram
    n, bins, patches = plt.hist(data, bin_number, density = True, facecolor = 'green')
    
    #plot best fit
    y = norm.pdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth = 2)
    
    #makes the plot readable
    plt.xlabel("Miles Traveled to Campus")
    plt.ylabel("Fraction of Students")
    plt.title(titlest)
    plt.savefig(string)
    plt.clf()
    plt.cla()
    
    return


main()