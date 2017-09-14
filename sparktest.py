import pyspark
sc = pyspark.SparkContext()

raw_data = sc.textFile("people.csv")
raw_data.take(4)
