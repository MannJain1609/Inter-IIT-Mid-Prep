

import pandas as pd                                                         # importing libraries
import numpy as np



data = pd.read_csv("data_final.csv", index_col=0)                           # importimg catalog_B file


data.shape
data.columns
data.head()


data1 = data.drop(["Unnamed: 12", "Unnamed: 13", "Unnamed: 14"], axis=1)



data1.shape                                                                 #remove rows 157 -289

data1


data2 = data1.dropna()                                                      # removing columns with na data 


data2.shape

data2


data2.columns

data2.columns = data2.columns.str.replace(' ', '')                          # removing extra space from column names



data2.columns


data2.describe()

data2.shape



df = pd.read_csv("data_final2.csv", index_col=0)                            # reading new Astro Sat data



df.head()



df.shape



df.columns



df = df.drop(["Unnamed: 12", "Unnamed: 13", "Unnamed: 14", "Unnamed: 15"], axis=1)  # removing irrelevant columns


df


df.columns = df.columns.str.replace(' ', '')                                        # reading new Astro Sat data




catalog = pd.concat([data2, df])                                                    # concatenating two catalog files of AstroSat data


catalog.head()


catalog.to_csv(r'C:\Users\iampa\ISRO\catalog_B.csv', index = False)                 # saving catalog file locally

