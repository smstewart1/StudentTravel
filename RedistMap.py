#import libraries
import pandas as pd 
import numpy as np 
import math

#main function
def main():
    courses = ["CHM-090", "CHM-151", "CHM-152", "CHM-251", "CHM-252"]
    campus = ["SNWC", "PHSC", "RTP", "EWC"]
    prob_campus = ["PSNWC", "PPHSC", "PRTP", "PEWC"]
    
    #read in fitting parameters
    df = pd.read_csv("CustomFit.csv")
    df2 = pd.read_csv("ProbRadii.csv")
    
    #build a dictionary of the different models
    keys = {"CHM-090": [], "CHM-130": [], "CHM-131": [], "CHM-131A": [], "CHM-151": [], "CHM-152": [], "CHM-251": [], "CHM-252": [], "SWC": [], "SNWC": [], "PHSC": [], "RTP": [], "EWC": []}
    for i in df.index:
        name = df["Course"][i]
        keys[name].append([df["x0"][i], df["s"][i]])
    
    #finds the probabilities based purely on the campus
    for i in range(0, 4):
        df2[prob_campus[i]] = model(df2[campus[i]], keys[campus[i]][0][0], keys[campus[i]][0][1])
    df2["PUnassignedCampus"] = 1 - df2["PSNWC"] - df2["PPHSC"] - df2["PRTP"] - df2["PEWC"]
    print(df2.head())
    
    #builds up each campus distribution map
    CSV_files = []
    for i in campus:
        name = f"{i}_distr.csv"
        df_temp = pd.DataFrame(list(zip(df2["Zip"], df2[i])), columns = ["Zip", "Radius"])
        df_temp.to_csv(name)
        CSV_files.append(name)
        del df_temp
        del name
        
    df2.to_csv("RedistByCampus.csv")
    del df2
    
    #returns probability for each course based on functions
    for j in CSV_files:
        campy = j[0:7]
        df_temp = pd.read_csv(j)
        for i in courses:
            df_temp[i] = model(df_temp["Radius"], keys[i][0][0], keys[i][0][1])
        new_name = f"{campy}_with_courses.csv"
        df_temp.to_csv(new_name)
        del new_name
        del df_temp
    
    return
       
#additional functions
def model(x, x0, s):
    return (1 / (x * s * np.sqrt(2 * 3.141))) * np.exp(-((np.log(x) -x0) ** 2)/(2 * (s ** 2)))


main()