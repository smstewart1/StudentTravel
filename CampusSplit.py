#import libraries
import pandas as pd 
import numpy as np 
import scipy 
import math

#main function
def main():
    s_df = pd.read_csv("Zips.csv")
    z_df = pd.read_csv("NCZips.csv")
    merged_df = pd.merge(left = s_df, right = z_df, left_on = "Zip", right_on = "Zip")
        
    #calculate distances
    campuses = [["SWC", 35.65173 , -78.70469], ["SNWC", 35.86680, -78.54458], ["PHSC", 35.78525, -78.58441], ["RTP", 35.85326, -78.84055] , ["EWC", 35.52919, -78.30740]]
    for i in campuses:
        merged_df[i[0]] = 54.6 * ((i[1] - merged_df["Longitude"]) ** 2 + (i[2] - merged_df["Latitude"]) ** 2) ** 0.5 #converts distances to miles
    merged_df.to_csv("MergedStudents.csv")
    
    

#additional functions


main()