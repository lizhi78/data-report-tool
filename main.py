from pathlib import Path
import argparse

from loader import load_data, print_preview
from cleaner import clean_data


def main() -> None:
    parser = argparse.ArgumentParser(description="读取 CSV 或 Excel 数据并展示前几行与概况")
    parser.add_argument("--input", required=True, help="数据文件路径，支持 .csv / .xlsx / .xls")
    args = parser.parse_args()

    file_path = Path(args.input)
    df = load_data(file_path)

    print(f"已读取文件：{file_path}")
    print_preview(df)

    cleaned_df = clean_data(df)
    print("
清洗后数据：")
    print_preview(cleaned_df)


if __name__ == "__main__":
    main()
