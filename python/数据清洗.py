import pandas as pd
df = pd.read_csv("./python/data/实习练习-销售脏数据.csv")

print(df.shape)
print(df.info())

df.columns=df.columns.str.strip()
df=df.dropna(how="all")
df=df.drop_duplicates(subset=df.columns,keep="first")



df["数量"]=df["数量"].astype(str).str.strip().str.replace("个","",regex=False)#regex=False 的含义：告诉 Pandas 这里 "个" 是普通文字，不是正则表达式。如果不写，新版本的 Pandas 会报警告，因为它默认把第一个参数当成正则规则。
df["数量"]=pd.to_numeric(df["数量"],errors="coerce")
df["单价(元)"]=df["单价(元)"].astype(str).str.strip().str.replace("元","",regex=False).str.replace(",","",regex=False)
df["单价(元)"]=pd.to_numeric(df["单价(元)"],errors="coerce")
df["销售额"]=pd.to_numeric(df["销售额"],errors="coerce")



# 1. 复制原始文本，新增一列【备份原始日期字符串】
df["Date_original"] = df["Date"]
# 2. 原地覆盖 Date 列，转为标准 datetime；解析失败 → NaT
df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")
# 3. 新增布尔标记列，标识本行日期是否解析成功
df ["is_date_valid"] = df ["Date"].notna ()
'''
df["Date"]=pd.to_datetime(df["Date"],format="mixed",errors="coerce")
df=df.dropna(subset=["Date"])
#第一行代码的作用是将不同格式的时日期表示全都转换成统一标准的pandas的日期表示格式datetime64,并将转换失败的(如2026-2-30，abc,8月23日等其他格式)变成NaT
#第二行代码的作用是查找Date列为空(NaT)的行删除这一整行
# 两行代码结合起来就是智能转换Date格式，转换不成功的标记为空，再将所有Date列为空的行删除
'''



异常行=(df["数量"]>1000)|(df["数量"]<=0)|(df["单价(元)"]<=0)

df.loc[~异常行,"销售额"]=df.loc[~异常行,"数量"]*df.loc[~异常行,"单价(元)"]
#~异常行是异常行取非操作也就是正常行
df["数量"] = df["数量"].astype(object)
df["单价(元)"] = df["单价(元)"].astype(object)
df["销售额"] = df["销售额"].astype(object)
#三列转成文本类型，再写"异常"（避免数字列写字符串报warning
#pandas 中：一列原本是纯数值类型（int64 / float64），只能存放数字、NaN。如果你强行往这一列写入字符串（"异常"、"未知"）：数值类型无法存储文本。pandas 为了兼容，自动把整列的数据类型强制转换成 object（混合类型）
df.loc[异常行,"数量"]="异常"
df.loc[异常行,"单价(元)"]="异常"
df.loc[异常行,"销售额"]="异常"


df=df.fillna("未知")


df["销售额_数字"] = pd.to_numeric(df["销售额"],errors="coerce")#创建全新额外一列 `销售额_数字`，临时存在的
#将销售额临时存为数字方便以后的计算.sum
print("按类别汇总")
stat_category=df.groupby("类别")["销售额_数字"].sum().sort_values(ascending=False).reset_index()#.reset_index()将0，1，2...的索引重新赋给它
stat_category.columns=["类别", "销售额合计"]#给表头名称
print(stat_category)
print("按地区汇总")
stat_region=df.groupby("地区")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
stat_region.columns=["地区", "销售额合计"]#给表头名称
print(stat_region)
print("按销售员汇总")
stat_sales=df.groupby("销售员")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
stat_sales.columns=["销售员", "销售额合计"]
print(stat_sales)
df=df.drop(columns=["销售额_数字"])#删除这个临时的series
print(df)



#导出成不同sheet的excel（要用pd.ExcelWriter)
df["Date"] = pd.to_datetime(df["Date"],format="mixed", errors="coerce").dt.strftime("%Y-%m-%d")#原始文本 → pd.to_datetime → datetime时间类型 → .dt.strftime → 普通字符串str
# 开启Excel写入通道
with pd.ExcelWriter("./python/data/销售数据结果.xlsx",engine="openpyxl")as writer:
    # 第一个工作表
    df.to_excel(writer, sheet_name="清洗明细",index=False)
    # 第二个工作表
    stat_category.to_excel(writer, sheet_name="按类别统计",index=False)#index=False说明不要索引0123...
    # 第三个工作表
    stat_region.to_excel(writer, sheet_name="按地区统计",index=False)
    # 第四个工作表
    stat_sales.to_excel(writer, sheet_name="销售员统计",index=False)
# 代码走到这里，with块结束
# 自动：保存文件 + 关闭Excel资源
print(df.shape)
print("导出完成")





#将excel导出成Markdown
excel_path = "./python/data/销售数据结果.xlsx"  # 你的Excel文件路径
output_md = "./python/data/数据分析报告.md"



# 1. 获取Excel所有工作表名称
excel_file = pd.ExcelFile(excel_path)
sheet_names = excel_file.sheet_names

# 2. 开始组装markdown全文
md_content = "# 数据分析汇总报告\n\n"

# 循环遍历每一张sheet
for sheet in sheet_names:
    md_content += f"## {sheet}\n\n"
    # 读取当前工作表
    df = pd.read_excel(excel_path, sheet_name=sheet)
    # DataFrame转markdown表格，index=False去掉索引
    table_md = df.to_markdown(index=False)
    md_content += table_md
    md_content += "\n\n"  # 表格之间空行分隔

# 3. 保存成md文件
with open(output_md, "w", encoding="utf-8-sig") as f:
    f.write(md_content)

print("Markdown报告生成完成！")






import json
import pandas as pd
from datetime import datetime
from llm_api import chat_with_ai 

def safe_json_dumps(data):
    def convert_obj(obj):
        if isinstance(obj, (pd.Timestamp, datetime)):
            return str(obj)
        if isinstance(obj, (pd.Series, pd.DataFrame)):
            return obj.to_dict()
        # numpy数字类型转换
        if hasattr(obj, "item"):
            return obj.item()
        raise TypeError(f"无法序列化对象 {type(obj)}")
    return json.dumps(data, default=convert_obj, ensure_ascii=False, indent=2)

# ========== 使用部分 =========
stat_info = {
    "总行数": len(df),
    "列名": df.columns.tolist(),
    "缺失值数量": df.isna().sum().to_dict(),
    "数值字段统计": df.describe().to_dict()
}

stat_json_str = safe_json_dumps(stat_info)

prompt = f"""
下面是数据集统计结果：
{stat_json_str}
根据这份数据写一段通顺、正式的数据分析文字，不要编造信息，只客观解读指标。
"""

result = chat_with_ai(prompt)
print(result)
