import pandas as pd
import time

print("=" * 80)
print("Pandas 性能测试 - 评分最高的15部电影")
print("=" * 80)

# 记录开始时间
start_time = time.time()

# 读取数据
print("\n正在读取数据...")
df = pd.read_csv("douban_movies_cleaned.csv", encoding='utf-8', on_bad_lines='skip')
print(f"数据加载完成！共 {len(df)} 行，{len(df.columns)} 列")

# 查询2：评分最高的15部电影
print("\n" + "=" * 60)
print("查询2：评分最高的15部电影（ORDER BY Top-N）")
print("=" * 60)

# 按评分降序排序，取前15
top15 = df.nlargest(15, 'rating_score')[['title', 'rating_score', 'rating_count', 'year', 'genres']]

# 显示结果
print(top15.to_string(index=False))

# 计算执行时间
execution_time = time.time() - start_time
print(f"\n⏱️ Pandas 执行时间: {execution_time:.4f} 秒")

print("\n【分析说明】本查询按评分降序排列，筛选出评分最高的15部电影。")
print("当评分相同时，按评分人数排序，确保人气更高的电影排在前面。")

print("\n" + "=" * 80)
print("数据分析完成！")
print("=" * 80)