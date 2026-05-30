from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCount").getOrCreate()

# 读取测试数据
lines = spark.sparkContext.parallelize([
    "hello world spark",
    "hello spark operator",
    "spark on kubernetes is great",
    "hello hello hello"
])

word_counts = (
    lines.flatMap(lambda line: line.split())
         .map(lambda word: (word, 1))
         .reduceByKey(lambda a, b: a + b)
         .sortBy(lambda x: x[1], ascending=False)
)

print("Top 10 words:", word_counts.take(10))
spark.stop()