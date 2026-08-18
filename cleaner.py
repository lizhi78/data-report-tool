import re

import pandas as pd


def _normalize_date_value(value):
    """把如 2026/8/2、8月3日、2026-07-07 统一成可解析的字符串。"""
    if pd.isna(value):
        return pd.NaT

    text = str(value).strip()
    if text in {"", "nan", "None", "NULL"}:
        return pd.NaT

    text = text.replace("年", "-").replace("月", "-").replace("日", "")
    text = text.replace("/", "-")
    text = re.sub(r"\s+", "", text)

    # 2026-07-07 这样的日期无需修改
    # 8-3 这种只有月日，需要补上年份
    if re.fullmatch(r"\d{1,2}-\d{1,2}", text):
        text = f"2026-{text}"

    return text


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """清洗脏数据：删除全空行、重复行，统一日期格式，并将数字列转为数值类型。"""
    df = df.copy()

    # 1）处理表头和每个单元格中的空格
    df.columns = [str(col).strip() for col in df.columns]
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    # 2）删除一整行全为空的记录
    df = df.dropna(how="all")

    # 3）删除完全重复的记录
    df = df.drop_duplicates()

    # 4）统一日期格式：支持 2026/8/2、8月3日、2026-07-07 等
    if "Date" in df.columns:
        df["Date"] = df["Date"].map(_normalize_date_value)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 5）清洗“数量”“单价(元)”“销售额”：删除单位、空格、逗号
    for col in ["数量", "单价(元)", "销售额"]:
        if col in df.columns:
            df[col] = df[col].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].str.replace(r"[\s,￥元个]", "", regex=True)
            df[col] = df[col].str.replace(r"[^0-9.\-]", "", regex=True)
            df[col] = df[col].replace("", pd.NA)

    # 6）将字符串数字转成数值类型
    if "数量" in df.columns:
        df["数量"] = pd.to_numeric(df["数量"], errors="coerce").astype("Int64")

    if "单价(元)" in df.columns:
        df["单价(元)"] = pd.to_numeric(df["单价(元)"], errors="coerce").astype(float)

    if "销售额" in df.columns:
        df["销售额"] = pd.to_numeric(df["销售额"], errors="coerce").astype(float)

    return df
