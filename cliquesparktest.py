from pyspark import SparkContext, SQLContext
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf, array
from pyspark.sql import functions as f
import udfsimCompare
import ast
import pandas as pd
from itertools import product

sc = SparkContext()
sqlContext = SQLContext(sc)

NUM_OF_USERS = 7

df = sqlContext.read.csv("fakeresults.csv", header=True)
pddf = pd.read_csv("fakeresults.csv", converters={1:ast.literal_eval})

pddf = pd.DataFrame([[0,.9,.9,.9,.8,.2,.2],
                     [0,0,.9,.9,.2,.2,.2],
                     [0,0,0,.9,.2,.2,.2],
                     [0,0,0,0,.2,.2,.2],
                     [0,0,0,0,0,.8,.8],
                     [0,0,0,0,0,0,.8],
                     [0,0,0,0,0,0,0]])



print(df)
df.show()

print(pddf.head())





def findGroups(pddf):
    groups = [[], [], [], [], [], [], []]
    for i in range(0,NUM_OF_USERS-1):
        for j in range(i+1, NUM_OF_USERS):
            print(pddf[j][i])
            if pddf[j][i] > .2:
                groups[i].append(j+1)
                groups[j].append(i+1)
    return groups


group = findGroups(pddf)
print(group)
