#import libraries
import pandas as pd 
import numpy as np 
import math

#main function
def main():
    campus = ["SNWC", "PHSC", "RTP", "EWC"]
    prob_campus = ["PSNWC", "PPHSC", "PRTP", "PEWC"]
    
    #read in fitting parameters
    df = pd.read_csv("CustomFit.csv")
    
    
    #build a dictionary of the different models
    keys = {"CHM-090": [], "CHM-130": [], "CHM-131": [], "CHM-131A": [], "CHM-151": [], "CHM-152": [], "CHM-251": [], "CHM-252": [], "SWC": [], "SNWC": [], "PHSC": [], "RTP": [], "EWC": []}
    for i in df.index:
        name = df["Course"][i]
        keys[name].append([df["x0"][i], df["s"][i]])
           
    #read in raw data
    df2 = pd.read_csv("MergedStudents.csv")
    df3 = pd.read_csv("ProbRadii.csv")
        
        #look at percentage change as a function of year-term (YT)
    #cleans up the merged students data frame
    for i in campus:
        df2 = df2.drop(columns = i)
    df2 = df2.drop(columns = 'SWC')
    df2 = df2.drop(columns = 'Longitude')
    df2 = df2.drop(columns = 'Latitude')
    df2 = df2.drop(columns = "Student")
    df2 = df2.drop(columns = "RadiusHC")
    df2 = df2.drop(columns = "Gender")
    df2 = df2.drop(columns = "Ethnicity")
    df2 = df2.drop(columns = "Delivery")
    df2["BodyCount"] = 1
    
    #finds the probabilities based purely on the campus
    for i in range(0, 4):
        df3[prob_campus[i]] = model(df3[campus[i]], keys[campus[i]][0][0], keys[campus[i]][0][1])
    df3["PUnassignedCampus"] = 1 - df3["PSNWC"] - df3["PPHSC"] - df3["PRTP"] - df3["PEWC"]
    for i in campus:
        df3 = df3.drop(columns = i)
    
    #renames columns
    for i in range(0, len(campus)):
        df3 = df3.rename(columns = {prob_campus[i] : campus[i]})
    
    #calcualted the number of SWC students that woudl go to each campus by year-term
    df4 = df2[df2["Campus"] == "SWC"]
    df4a = pd.merge(df4, df3, left_on = "Zip", right_on = "Zip")
    
    #student loss by year-term
    loss_df = df4a.groupby(["YT"], as_index = False)["PUnassignedCampus"].sum()
    loss_df2 = df4a.groupby(["YT"], as_index = False)["PUnassignedCampus"].count()
    loss_df = pd.merge(loss_df, loss_df2, left_on = "YT", right_on = "YT")
    loss_df.columns = ["YT", "Loss", "Total"]
    loss_df["PerLoss"] = loss_df["Loss"]/loss_df["Total"]
    loss_df.to_csv("LossYT.csv")
    
    #build up the number of transfers by campus
    SNWC = df4a.groupby(["YT"], as_index = False)["SNWC"].sum()
    EWC = df4a.groupby(["YT"], as_index = False)["EWC"].sum()
    RTP = df4a.groupby(["YT"], as_index = False)["RTP"].sum()
    PHSC = df4a.groupby(["YT"], as_index = False)["PHSC"].sum()
    

    #adds the transfers to the existing enrollments
    dfsubset = df2[df2["Campus"] != "SWC"]
    dfcut = dfsubset.groupby(["YT", "Campus", "Year", "Term"], as_index = False)["BodyCount"].sum()
    RSNWC = dfcut[dfcut["Campus"] == "SNWC"]
    RRTP = dfcut[dfcut["Campus"] == "RTP"]
    RPHSC = dfcut[dfcut["Campus"] == "PHSC"]
    
    SNWCdf = pd.merge(RSNWC, SNWC, left_on = "YT", right_on = "YT")
    SNWCdf.columns = ["YT", "Campus", "Year", "Term", "Normal Enrollment", "Additional"]
    SNWCdf["Percent Change"] = SNWCdf["Additional"]/SNWCdf["Normal Enrollment"]
    PHSCdf = pd.merge(RPHSC, PHSC, left_on = "YT", right_on = "YT")
    PHSCdf.columns = ["YT", "Campus", "Year", "Term", "Normal Enrollment", "Additional"]
    PHSCdf["Percent Change"] = PHSCdf["Additional"]/PHSCdf["Normal Enrollment"]
    RTPdf = pd.merge(RRTP, RTP, left_on = "YT", right_on = "YT")
    RTPdf.columns = ["YT", "Campus", "Year", "Term", "Normal Enrollment", "Additional"]
    RTPdf["Percent Change"] = RTPdf["Additional"]/RTPdf["Normal Enrollment"]
    
    #build up the EWC transfers
    EWCdf = pd.merge(EWC, RTPdf, left_on = "YT", right_on = "YT")
    EWCdf.drop(columns = ["Campus", "Additional", "Normal Enrollment", "Percent Change"], inplace = True)
    EWCdf.columns = ["YT", "Additional Students", "Year", "Term"]
    
    final_comple = pd.concat([SNWCdf, PHSCdf, RTPdf], axis = 0)
    final_comple.to_csv("FinalChanges.csv")
    EWCdf.to_csv("EWCFinalChanges.csv")
    
    return


#modeling function
def model(x, x0, s):
    return (1 / (x * s * np.sqrt(2 * 3.141))) * np.exp(-((np.log(x) -x0) ** 2)/(2 * (s ** 2)))

main()