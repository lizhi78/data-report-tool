#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py -- 程序入口（F9：命令行参数 + 全流程调度）

用法：
    python main.py --input data.xlsx --output ./output/
    python main.py -i ./data/sales.csv -o ./result/
"""

import argparse
import sys
import os

import pandas as pd
from loader import load_data, print_preview
from cleaner import clean_data
from analyzer import abnormal_data, statistic_data


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="数据清洗流水线"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="输入文件路径，支持 .csv / .xlsx / .xls"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出目录路径，清洗后的文件会保存在这里"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    input_path = args.input
    output_dir = args.output

    # 检查输入文件是否存在
    if not os.path.isfile(input_path):
        print(f"错误：找不到文件 {input_path}")
        sys.exit(1)

    # 创建输出目录（如果不存在就自动创建）
    os.makedirs(output_dir, exist_ok=True)

    try:
        # ---------- 第1步：加载数据 ----------
        print(">>> 正在加载数据...")
        df = load_data(input_path)



        df = load_data(input_path)
    
        # ===== 排查代码 =====
        print("\n【原始数据单价检查】")
        print(f"单价列的数据类型：{df['单价(元)'].dtype}")
        print(f"单价列唯一值（前30个）：{df['单价(元)'].unique()[:30]}")
        print(f"单价为1的行数：{(df['单价(元)'] == '1').sum() + (df['单价(元)'] == 1).sum()}")
        print("原始数据里单价为1的样本：")
        print(df[df["单价(元)"].isin([1, '1'])][["数量", "单价(元)", "销售额", "Date"]].head())
        # ====================






        print(f"加载完成：{len(df)} 行 x {len(df.columns)} 列")
        print_preview(df)

        # ---------- 第2步：清洗数据 ----------
        print(">>> 正在清洗数据...")
        df_cleaned, report = clean_data(df)
        print("清洗完成")

        # ---------- 第3步：异常处理 ----------
        print(">>> 正在处理异常数据...")
        df_abnormal = abnormal_data(df_cleaned)
        print("异常处理完成（异常值已标记为'异常'）")

        # ---------- 第4步：统计分析 ----------
        print(">>> 正在进行统计分析...")
        df_final, stats_dict = statistic_data(df_abnormal)
        print("统计分析完成")

        # 准备文件名（去掉扩展名）
        file_name = os.path.splitext(os.path.basename(input_path))[0]

        # ---------- 第5步：保存结果 ----------

        # 5.1 保存异常处理后的主数据
        output_main = os.path.join(output_dir, f"清洗后_{file_name}.xlsx")
        df_final.to_excel(output_main, index=False)
        print(f"主数据已保存：{output_main}")

        # 5.2 保存统计报告（一个Excel文件，多个Sheet）
        stats_file = os.path.join(output_dir, f"统计报告_{file_name}.xlsx")
        with pd.ExcelWriter(stats_file, engine="openpyxl") as writer:
            for sheet_name, df_stat in stats_dict.items():
                # Excel 的 Sheet 名最长 31 个字符，超长就截断
                sheet = sheet_name[:31]
                df_stat.to_excel(writer, sheet_name=sheet, index=False)
        print(f"统计报告已保存：{stats_file}")

        # 5.3 保存文本报告
        report_path = os.path.join(output_dir, "处理报告.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("数据清洗与处理报告\n")
            f.write("=" * 40 + "\n")
            for key, value in report.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            f.write("说明：\n")
            f.write("- 异常数据已标记为'异常'，原销售额备份在'销售额_previous'列\n")
            f.write(f"- 统计报告（多Sheet）已保存至：统计报告_{file_name}.xlsx\n")
        print(f"文本报告已保存：{report_path}")

        print("\n全部完成！")

    except Exception as e:
        print(f"程序运行出错：{e}")
        import traceback
        traceback.print_exc()  # 打印详细错误信息，方便排查
        sys.exit(1)


if __name__ == "__main__":
    main()