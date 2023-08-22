#import libraries
import pandas as pd 
import numpy as np 
import math

#main function
def main():
    courses = ["CHM-090", "CHM-151", "CHM-152", "CHM-251", "CHM-252"]
    campus = ["SNWC", "PHSC", "RTP", "EWC"]
    
    #read in fitting parameters
    df = pd.read_csv("CustomFit.csv")
    
    #by course and campus
    df_C = pd.read_csv("SWC.csv")
       
    composite = []
    
    #start looking at each campus by course
    for j in range(0, 5):
        # read in model parameters
        fits = df[df["Course"] == courses[j]]
        temp = [courses[j]]
        for i in range(0, len(campus)):
            df_C[i] = model(df_C[campus[i]], fits["x0"].item(), fits["s"].item())
        for i in range(0, len(campus)):
            temp.append(df_C[i].sum() / df_C[i].count() * 100)
        composite.append(temp)
        del temp

    df_final = pd.DataFrame(composite, columns = ["Course", "SNWC", "PHSC", "RTP", "EWC"])
    df_final.to_csv("FinalProbsByCourse.csv")
    del df_final
    
    #start at the campus itself
    other_composite = []
    for j in range(0, 4):
        # read in model parameters
        fits = df[df["Course"] == campus[j]]
        temp = [campus[j]]
        df_C[i] = model(df_C[campus[i]], fits["x0"].item(), fits["s"].item())
        temp.append(df_C[i].sum() / df_C[i].count() * 100)
        other_composite.append(temp)
        del temp
    

    df_final = pd.DataFrame(other_composite, columns = ["Campus", "Percentage of Students"])
    df_final.to_csv("FinalProbsByCampus.csv")
    

#additional functions
def model(x, x0, s):
    return (1 / (x * s * np.sqrt(2 * 3.141))) * np.exp(-((np.log(x) -x0) ** 2)/(2 * (s ** 2)))


main()