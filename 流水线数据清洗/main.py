#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from loader import load_data, print_preview
from cleaner import clean_data
from analyzer import abnormal_data, statistic_data
import ai_report
import exporter


# ---------- 第0步：读取命令行参数 ----------
parser = argparse.ArgumentParser(description="数据清洗流水线")#创建命令行参数解释器
#传入两个参数
parser.add_argument("--input", "-i", required=True, help="输入文件路径")#-i 就只是 --input 的简写,required=True表示这个参数代表的值是必须要有的，如果你不写这个参数，程序就会报错。help="输入文件路径" 这个参数的作用是，当你在终端敲 python main.py -h 时，会显示这个参数的作用说明。
parser.add_argument("--output", "-o", required=True, help="输出目录路径")#-o 就只是 --output 的简写

args = parser.parse_args()#把用户输入的命令拆解，打包进 args；读取你终端敲的一整行命令,把`‑i`后面的值拿出来，存到`args.input`,把`‑o`后面的值拿出来，存到`args.output`；
input_path = args.input
output_dir = args.output

if not os.path.isfile(input_path):#判断这个路径，是不是真实存在的文件。
    print(f"错误：找不到文件 {input_path}")
    sys.exit(1)#如果找不到，立刻终止整个 Python 程序。

os.makedirs(output_dir, exist_ok=True)#os.makedirs创建文件夹, exist_ok=True表示如果文件夹已经存在，就不报错，继续往下执行。

#步骤1到4就是流水线清洗数据的过程，不断调用我已经写好的.py文件对数据进行加工
# ---------- 第1步：加载数据 ----------
print(">>> 正在加载数据...")
df = load_data(input_path)
print(f"加载完成：{len(df)} 行 x {len(df.columns)} 列")
print_preview(df)


# ---------- 第2步：清洗数据 ----------
print(">>> 正在清洗数据...")
df_cleaned, report = clean_data(df)#返回的是清洗好的df(日期统一，数量，单价(元)和销售额转换成Float类型)和清洗报告report
print("清洗完成")


# ---------- 第3步：异常处理 ----------
print(">>> 正在处理异常数据...")
df_abnormal = abnormal_data(df_cleaned)
print("异常处理完成")


# ---------- 第4步：统计分析 ----------
print(">>> 正在进行统计分析...")
df_final, stats_dict = statistic_data(df_abnormal)
print("统计分析完成")


# ---------- 第5步：AI 生成人话报告 ----------
print(">>> 正在调用 AI...")

data = ""
for name, table in stats_dict.items():
    data += f"\n{name}：\n{table.to_string(index=False)}\n"

r = ai_report.chat_with_ai(
    f"基于以下数据写人话分析（有结论建议，不罗列数字），返回JSON：{{'analysis': '内容'}}\n\n{data}"
)

if r["status"]:                                    # 如果调用成功
    ai_analysis = r["data"].get("analysis", "无内容")  # 从 data 里取 analysis，没有就写"无内容"
else:                                              # 如果调用失败
    ai_analysis = r["msg"]                          # 把错误信息（如"请求超时"）当作分析文字
print("AI分析完成" if r["status"] else ai_analysis)


# ---------- 第6步：保存结果 ----------
file_name = os.path.splitext(os.path.basename(input_path))[0]

excel_path = os.path.join(output_dir, f"汇总_{file_name}.xlsx")
exporter.save_excel(df_final, stats_dict, excel_path)
print(f"Excel 已保存：{excel_path}")

md_path = os.path.join(output_dir, f"汇总_{file_name}.md")
exporter.save_markdown(file_name, stats_dict, ai_analysis, md_path)
print(f"Markdown 已保存：{md_path}")

print("\n全部完成！")