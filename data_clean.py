import pandas as pd
import numpy as np
import os

# 数据文件路径
file_path = "douban_movies_cleaned.csv"

# 如果清洗后文件已存在，读取原始数据
if not os.path.exists(file_path):
    file_path = "./data/douban_movies.csv"
    
df = pd.read_csv(file_path)

print("=" * 60)
print("数据清洗报告")
print("=" * 60)

# 1. 基本信息
print("\n【1. 数据基本信息】")
print(f"数据形状: {df.shape}")

print("\n字段数据类型:")
print(df.dtypes)

print("\n前5行数据:")
print(df.head())

# 2. 缺失值统计
print("\n【2. 缺失值统计】")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'缺失数量': missing, '缺失比例(%)': missing_pct})
print(missing_df)

# 3. 清洗前记录数
before = len(df)
print(f"\n【3. 清洗前】总记录数: {before}")

# 4. 处理缺失值
print("\n【4. 缺失值处理策略】")

# 策略1：评分缺失用中位数填充（数值型数据）
if 'rating_score' in df.columns:
    missing_count = df['rating_score'].isnull().sum()
    if missing_count > 0:
        median_val = df['rating_score'].median()
        df['rating_score'] = df['rating_score'].fillna(median_val)
        print(f"✓ rating_score（评分）: 用中位数 {median_val:.2f} 填充 - 原因：数值型连续数据，保留记录")
    else:
        print("✓ rating_score（评分）: 无缺失值")

# 策略2：年份缺失用中位数填充
if 'year' in df.columns:
    missing_count = df['year'].isnull().sum()
    if missing_count > 0:
        median_year = df['year'].median()
        df['year'] = df['year'].fillna(median_year)
        print(f"✓ year（年份）: 用中位数 {median_year:.0f} 填充 - 原因：时间数据，中位数代表典型年份")

# 策略3：类型缺失则删除（分类变量，缺失比例约8%）
if 'genres' in df.columns:
    before_genre = len(df)
    df = df.dropna(subset=['genres'])
    after_genre = len(df)
    removed = before_genre - after_genre
    if removed > 0:
        print(f"✓ genres（类型）: 删除缺失行 ({removed} 行) - 原因：分类变量无法合理填充，删除比例低")
    else:
        print("✓ genres（类型）: 无缺失值")

# 策略4：导演缺失填充为"未知"（分类变量）
if 'directors' in df.columns:
    missing_count = df['directors'].isnull().sum()
    if missing_count > 0:
        df['directors'] = df['directors'].fillna('未知')
        print(f"✓ directors（导演）: 用'未知'填充 ({missing_count} 行) - 原因：保留记录，便于后续分析")
    else:
        print("✓ directors（导演）: 无缺失值")

# 5. 清洗后记录数
after = len(df)
print(f"\n【5. 清洗后】总记录数: {after}")
print(f"删除行数: {before - after} (占比 {(before-after)/before*100:.2f}%)")
print(f"保留行数: {after} (占比 {after/before*100:.2f}%)")

# 6. 数值字段统计信息
print("\n【6. 数值字段统计信息 (mean/std/min/max)】")
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    print(f"\n{col}:")
    print(f"  平均值 (mean): {df[col].mean():.2f}")
    print(f"  标准差 (std): {df[col].std():.2f}")
    print(f"  最小值 (min): {df[col].min()}")
    print(f"  最大值 (max): {df[col].max()}")

# 7. 保存清洗后的数据
output_path = "douban_movies_cleaned.csv"
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"\n【7. 数据保存】清洗后的数据已保存到: {output_path}")

print("\n" + "=" * 60)
print("数据清洗完成")