from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnan, when, count, mean, stddev, min, max, isnull
from pyspark.sql.types import *
import time

# 创建 SparkSession
spark = SparkSession.builder \
    .appName("DataCleaning") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# 读取 CSV 文件
print("正在读取数据...")
df = spark.read.csv("douban_movies_cleaned.csv", header=True, inferSchema=True)

print("=" * 60)
print("数据清洗报告")
print("=" * 60)

# 1. Schema 和前5行
print("\n【1. 数据基本信息】")
print("数据形状: {} 行, {} 列".format(df.count(), len(df.columns)))

print("\n字段数据类型 (Schema):")
df.printSchema()

print("\n前5行数据:")
df.show(5, truncate=50)

# 2. 缺失值统计
print("\n【2. 缺失值统计】")
total_count = df.count()
for col_name in df.columns:
    null_count = df.filter(col(col_name).isNull()).count()
    null_ratio = null_count / total_count * 100
    print(f"{col_name}: {null_count} / {total_count} ({null_ratio:.2f}%)")

# 3. 清洗前记录数
before_count = df.count()
print(f"\n【3. 清洗前】总记录数: {before_count}")

# 4. 处理缺失值
print("\n【4. 缺失值处理策略】")

# 策略1：评分用中位数填充（数值型）
if 'rating_score' in df.columns:
    # 计算中位数
    median_rating = df.select(mean('rating_score')).collect()[0][0]
    df = df.fillna({'rating_score': median_rating})
    print(f"✓ rating_score（评分）: 用平均值 {median_rating:.2f} 填充 - 原因：数值型数据，保留记录完整性")

# 策略2：年份用中位数填充
if 'year' in df.columns:
    median_year = df.select(mean('year')).collect()[0][0]
    df = df.fillna({'year': median_year})
    print(f"✓ year（年份）: 用平均值 {median_year:.0f} 填充 - 原因：时间数据，保持分布特征")

# 策略3：类型缺失则删除（分类变量）
if 'genres' in df.columns:
    before_genre = df.count()
    df = df.dropna(subset=['genres'])
    after_genre = df.count()
    removed = before_genre - after_genre
    print(f"✓ genres（类型）: 删除 {removed} 行缺失数据 - 原因：分类变量，无法合理填充")

# 策略4：导演缺失填充为"未知"
if 'directors' in df.columns:
    df = df.fillna({'directors': '未知'})
    print(f"✓ directors（导演）: 用'未知'填充 - 原因：保留记录，标记缺失值")

# 5. 清洗后记录数
after_count = df.count()
print(f"\n【5. 清洗后】总记录数: {after_count}")
print(f"删除行数: {before_count - after_count}")
print(f"保留行数: {after_count}")
print(f"保留比例: {after_count/before_count*100:.2f}%")

# 6. 数值字段统计信息
print("\n【6. 数值字段统计信息 (mean/std/min/max)】")
numeric_cols = [f.name for f in df.schema.fields if f.dataType.typeName() in ['integer', 'double', 'long']]
for col_name in numeric_cols:
    stats = df.select(
        mean(col_name).alias('mean'),
        stddev(col_name).alias('std'),
        min(col_name).alias('min'),
        max(col_name).alias('max')
    ).collect()[0]
    print(f"\n{col_name}:")
    print(f"  平均值 (mean): {stats['mean']:.2f}" if stats['mean'] else "  平均值: None")
    print(f"  标准差 (std): {stats['std']:.2f}" if stats['std'] else "  标准差: None")
    print(f"  最小值 (min): {stats['min']}")
    print(f"  最大值 (max): {stats['max']}")

# 7. 保存清洗后的数据
output_path = "douban_movies_cleaned_output.csv"
df.write.csv(output_path, header=True, mode="overwrite")
print(f"\n【7. 数据保存】清洗后的数据已保存到: {output_path}")

print("\n" + "=" * 60)
print("数据清洗完成")

spark.stop()