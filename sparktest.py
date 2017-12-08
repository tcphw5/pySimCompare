from pyspark import SparkContext, SQLContext
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf, array
from pyspark.sql import functions as f
import udfsimCompare
import ast
import pandas as pd
from itertools import product
from timeit import default_timer as timer

sc = SparkContext()
sqlContext = SQLContext(sc)

df4 = pd.read_csv('genPpl.csv', converters={1:ast.literal_eval})

#print("hi")
print(df4)

start = timer()

c = list(product(df4.personID.tolist(), df4.personID.tolist()))
dic = dict(zip(df4.personID, df4.traj))
df = pd.DataFrame(c, columns=['id', 'id2'])
df[['value1', 'value2']]=df.apply(lambda x:x.map(dic))
df = df.loc[df.id!=df.id2,:]

print(df)

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
print(spark_df.count())

pysim = udf(lambda val1, val2, lvl: udfsimCompare.simScorePairTest(val1, val2, lvl), DoubleType())

new_spark = spark_df.withColumn('Result', pysim('value1', 'value2', 'lvl'))

print(new_spark.show())

group_spark = new_spark.groupBy('idkey')
group_spark = group_spark.agg(f.sum('Result'))

# for removing scores that are too low
# group_spark = group_spark.filter(group_spark['sum(Result)'] > .2)

end = timer()

print(group_spark.show())
print(end - start)

# for testing

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

# shows how to filter out below a certain threshold
for x in most_sim_groups:
    print(x.filter(x['sum(Result)'] > 2).show())
