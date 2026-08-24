from pathlib import Path
import pandas as pd


def load_data(file_path:Path) -> pd.DataFrame:
    """读取 CSV 或 Excel 文件，并返回 pandas DataFrame。"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"不支持的文件格式：{suffix}，仅支持 .csv / .xlsx / .xls")

    return df

def print_preview(df: pd.DataFrame) -> None:
    """打印前几行和数据概况。"""
    print("前 5 行数据：")
    print(df.head(5))

    print("\n数据概况：")
    print(df.info())
