from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, max, min, desc, row_number, floor
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("DoubanAnalysis").getOrCreate()

print("=" * 80)
print("豆瓣电影数据分析报告")
print("=" * 80)

# 从 OBS 读取数据
df = spark.read.csv("s3a://bronya-land/douban_movies_cleaned_new.csv", 
                    header=True, inferSchema=True)

print(f"\n数据加载成功！共 {df.count()} 行")

# 查询1：各年份电影数量与平均评分
print("\n" + "=" * 80)
print("查询1：各年份电影数量与平均评分（GROUP BY 聚合）")
print("=" * 80)

year_stats = df.groupBy("year").agg(
    count("movie_id").alias("电影数量"),
    avg("rating_score").alias("平均评分"),
    max("rating_score").alias("最高评分"),
    min("rating_score").alias("最低评分")
).filter(col("year").isNotNull()).orderBy(col("year").desc())

year_stats.show(20, truncate=False)

print("\n【分析说明】按年份分组统计电影数量和平均评分，可以看出电影产量的变化趋势。")

# 查询2：评分最高的15部电影
print("\n" + "=" * 80)
print("查询2：评分最高的15部电影（ORDER BY Top-N）")
print("=" * 80)

top15 = df.filter(col("rating_score").isNotNull()) \
    .orderBy(desc("rating_score"), desc("rating_count")) \
    .limit(15)

top15.select("title", "rating_score", "rating_count", "year", "genres").show(15, truncate=False)

print("\n【分析说明】按评分降序排列，筛选出评分最高的15部电影。")

# 查询3：各年代电影数量与评分趋势
print("\n" + "=" * 80)
print("查询3：各年代电影数量与评分趋势（时间维度分析）")
print("=" * 80)

df_with_decade = df.withColumn("年代", floor(col("year") / 10) * 10)

decade_stats = df_with_decade.groupBy("年代").agg(
    count("movie_id").alias("电影数量"),
    avg("rating_score").alias("平均评分")
).filter(col("年代").isNotNull()).orderBy("年代")

decade_stats.show(20, truncate=False)

print("\n【分析说明】按年代分组，统计电影产量和平均评分的变化趋势。")

# 查询4：每年评分前5的电影
print("\n" + "=" * 80)
print("查询4：每年评分前5的电影（窗口函数 - 分区内排名）")
print("=" * 80)

window_spec = Window.partitionBy("year").orderBy(desc("rating_score"), desc("rating_count"))
ranked_movies = df.withColumn("rank", row_number().over(window_spec)) \
    .filter(col("rank") <= 5) \
    .orderBy("year", "rank")

ranked_movies.select("title", "year", "rating_score", "rating_count", "genres", "rank").show(50, truncate=False)

print("\n【分析说明】使用窗口函数 row_number() 按年份分区，对每年内的电影按评分排名。")

spark.stop()
print("\n" + "=" * 80)
print("数据分析完成！")
print("=" * 80)