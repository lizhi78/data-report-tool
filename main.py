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

from loader import load_data, print_preview
from cleaner import clean_data


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

    if not os.path.isfile(input_path):
        print(f"错误：找不到文件 {input_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    try:
        print(">>> 正在加载数据...")
        df = load_data(input_path)
        print(f"加载完成：{len(df)} 行 x {len(df.columns)} 列")

        print_preview(df)

        print(">>> 正在清洗数据...")
        df_cleaned, report = clean_data(df)

        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"清洗后_{file_name}.xlsx")

        df_cleaned.to_excel(output_path, index=False)
        print(f"清洗结果已保存：{output_path}")

        report_path = os.path.join(output_dir, "清洗报告.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("数据清洗报告\n")
            f.write("=" * 40 + "\n")
            for key, value in report.items():
                f.write(f"{key}: {value}\n")
        print(f"清洗报告已保存：{report_path}")

        print("全部完成！")

    except Exception as e:
        print(f"程序运行出错：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()