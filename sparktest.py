from pyspark import SparkContext, SQLContext
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf, array
from pyspark.sql import functions as f
sc = SparkContext()
sqlContext = SQLContext(sc)

import udfsimCompare
import ast
import pandas as pd

from itertools import product

#df = sqlContext.read.csv("ppl2.csv", header=True)
#df = sc.parallelize(df)
#df = df.select(df.personID.cast(DoubleType()), df.locID.cast(DoubleType()), df.stayTime.cast(DoubleType()), df.travelTime.cast(DoubleType()))

#[(3,2,3,1), (0,5.0,3.5,4.5,2.5,5.5,0)], [(5,1,2,4), (0,2.5,3.0,4.0,1.5,1.5,0)]]

data = [[(3,2,3,1), (0,5.0,3.5,4.5,2.5,5.5,0)], [(5,1,2,4), (0,2.5,3.0,4.0,1.5,1.5,0)]]

df = pd.DataFrame(data=data, columns=["loc", "times"])
df2 = pd.read_csv("ppl2.csv", converters={1:ast.literal_eval})

df["traj"] = df[["loc", "times"]].values.tolist()
df2["traj"] = df2[["loc", "times"]].values.tolist()
df3 = pd.DataFrame(df2[["personID", "traj"]])
df4 = pd.read_csv('ppl3.csv', converters={1:ast.literal_eval})



print("hi")
print(df4)
c = list(product(df4.personID.tolist(), df4.personID.tolist()))
dic = dict(zip(df4.personID, df4.traj))
df = pd.DataFrame(c, columns=['id', 'id2'])
df[['value1', 'value2']]=df.apply(lambda x:x.map(dic))
df = df.loc[df.id!=df.id2,:]

#print(df)

df['idkey'] = df['id'].astype(str) + ":" + df['id2'].astype(str)
del df['id']
del df['id2']

dfcopy = df.copy()
df['lvl'] = 1
dfcopy['lvl'] = 2

df = df.append(dfcopy, ignore_index=True)

print(df)



spark_df = sqlContext.createDataFrame(df)
print(spark_df.show())
#print(spark_df.take(1))
print(spark_df.count())

pysim = udf(lambda val1, val2, lvl: udfsimCompare.simScorePairTest(val1, val2, lvl), DoubleType())

new_spark = spark_df.withColumn('Result', pysim('value1', 'value2', 'lvl'))

print(new_spark.show())

group_spark = new_spark.groupBy('idkey')
group_spark = group_spark.agg(f.sum('Result'))

print(group_spark.show())

most_sim_groups = []
currentGroup = []
sameXValGroup = []

for x in range(1, 5):
    sameXValGroup = []
    targetID = f"{x}:%"
    currentGroup = group_spark.filter(group_spark.idkey.like(targetID))
    print(currentGroup.show())

    most_sim_groups.append(currentGroup)

print(most_sim_groups)

for x in most_sim_groups:
    print(x.filter(x['sum(Result)'] > 2).show())
#print(df.head())

#print(df3)