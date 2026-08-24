import pandas as pd
path=r"C:\Users\wutia\Desktop\实习练习-销售脏数据.csv"
df = pd.read_csv(path)
print(df.isnull().sum(axis=0))#遍历每一列有几个空白数据，如果改成axis=1则遍历每一列有几个空白数据
print(df[df.isnull().any(axis=1)])#axis=1按行查询，axis=0按列查询
print(df.info())
print(df.describe())

print(df.loc[0:5])#读取下标索引值为0到5的六行
print(df["订单编号 "])#读取列的名称为订单编号 的这一整列

df = df.set_index("订单编号 ", inplace=False)#用订单编号 代替索引值
print(df.head())
# 将数量列转为数字，错误内容变成NaN
df["数量"] = pd.to_numeric(df["数量"], errors="coerce")

# 同样处理单价列
df["单价(元)"] = pd.to_numeric(df["单价(元)"], errors="coerce")

# 条件筛选
mask = (df["数量"] >= 10) & (df["单价(元)"] > 50)
result = df[mask]
print(result)

print(df[mask])



'''
df.sort_values(
    by="列名",#填写要排序的列名称
    ascending=True,#`True`= 升序（从小到大，默认）；`False`= 降序（从大到小）
    inplace=False,#是否原地修改 DataFrame；
    na_position="last"#空值放在哪里；`"last"`放末尾（默认），`"first"`放最前面
)
`sort_values()` 默认不会改动原始 df，必须用变量接收返回结果！
'''

'''
import pandas as pd
print("========= 1.1 只用列表创建Series（默认数字索引 0,1,2,3）========")
# 1.1 仅有数据列表产生最简单的Series
s1 = pd.Series([1, 'a', 5.2, 7])
print("s1 完整内容：")
print(s1)
print("s1 的索引：", s1.index)
print("s1 的数据值：", s1.values)
print("-" * 50)

print("========= 1.2 自定义标签索引创建Series =========")
# 1.2 创建带有自定义标签索引的Series
s2 = pd.Series([1, 'a', 5.2, 7], index=['d', 'b', 'a', 'c'])
print("s2 完整内容：")
print(s2)
print("s2 的索引：", s2.index)
print("-" * 50)

print("========= 1.3 使用字典创建Series =========")
# 1.3 通过python字典构造Series
sdata = {'Ohio': 35000, 'Texas': 72000, 'Oregon': 16000, 'Utah': 5000}
s3 = pd.Series(sdata)
print("s3 完整内容：")
print(s3)
print("-" * 50)

print("========= Series取值操作（类似字典key查询）========")
# 根据标签取值演示（对应最后一张截图）
print("s2['a'] 单个取值结果：", s2['a'])
print("类型：", type(s2['a']))

# 传入列表，一次性取出多条数据（返回新的Series）
sub_series = s2[['b', 'a']]
print("\ns2[['b','a']] 多条取值结果：")
print(sub_series)
print("数据类型：", type(sub_series))





data = {
    'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
    'year': [2000, 2001, 2002, 2001, 2002],
    'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 打印查看结果
print(df)
'''