#import libraries
import pandas as pd 
import numpy as np 
import scipy 
import math

#main function
def main():
    df = pd.read_csv("MergedStudents.csv")
    
    campuses = df["Campus"].unique()
    courses = df["Course"].unique()
    
    for i in campuses:
        string = f"{i}.csv"
        df_temp = df.loc[df["Campus"] == i]
        df_temp.to_csv(string)
    
    for i in courses:
        string = f"{i}.csv"
        df_temp = df.loc[df["Course"] == i]
        df_temp.to_csv(string)

#additional functions


main()