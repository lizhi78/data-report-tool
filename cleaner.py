import re
import pandas as pd

def clean_data(df):
    # ==================== F3：清洗报告（记录每一步）====================
    report = {}#创建一个字典来存储清洗报告
    report["原始行数"] = len(df)
    report["原始列数"] = len(df.columns)

    # ---------- 1. 列名去空格 ----------
    df.columns = df.columns.str.strip()

    # ---------- 2. 删除全空行 ----------
    n = len(df)
    df = df.dropna(how="all")
    report["删除全空行"] = n - len(df)

    # ---------- 3. 删除重复行 ----------
    n = len(df)
    df = df.drop_duplicates(subset=df.columns, keep="first")
    report["删除重复行"] = n - len(df)

    # ---------- 4. 日期清洗 ----------
    # 先记住：哪些行原本就是空的
    date_was_empty = df["Date"].isna()
    report["日期原本缺失"] = date_was_empty.sum()#原本就缺失，是空值写入到report中

    def clean_date(text):
        # 把空值转成字符串处理并去掉前后空格
        text = str(text).strip()
        # 情况1："8月3日" → 补上年份 → "2026-8-3"
        if re.fullmatch(r'\d{1,2}月\d{1,2}日', text):
            nums = re.findall(r'\d+', text)
            return f'2026-{nums[0]}-{nums[1]}'
        # 情况2："2026/8/2" → 斜杠改横杠 → "2026-8-2"
        if re.fullmatch(r'\d{4}/\d{1,2}/\d{1,2}', text):
            return text.replace('/', '-')
        # 情况3："2026-07-07" → 已经是标准格式，直接返回即可
        if re.fullmatch(r'\d{4}-\d{1,2}-\d{1,2}', text):
            return text
        # 其他情况（如空值，非日期格式，无效日期等）直接返回原始文本
        else:
            return text

    df["Date"] = df["Date"].apply(clean_date)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 清洗后还是空的 = 格式错误 + 原本就空
    date_still_nat = df["Date"].isna()#在进行to_datetime转换后，仍然是空值的部分
    report["日期格式错误"] = (date_still_nat & ~date_was_empty).sum()#之前不是空值，转换后变成空值的部分，说明格式错误

    df["Date"] = df["Date"].astype(object)
    df.loc[date_still_nat & ~date_was_empty, "Date"] = "日期格式错误"   
    df.loc[date_still_nat & date_was_empty, "Date"] = "未知"

    # ---------- 5. 数值提取 ----------
    # 记录提取前有多少空值
    qty_na_before = df["数量"].isna().sum()
    report["数量原本缺失"] = qty_na_before
    price_na_before = df["单价(元)"].isna().sum()
    report["单价原本缺失"] = price_na_before

    df["数量"] = df["数量"].astype(str).str.extract(r'(\d+)')[0]
    df["数量"] = pd.to_numeric(df["数量"], errors="coerce")
    df["单价(元)"] = df["单价(元)"].astype(str).str.extract(r'(\d+)')[0]
    df["单价(元)"] = pd.to_numeric(df["单价(元)"], errors="coerce")

    # 提取后新产生的空值 = 提取失败
    report["数量提取失败"] = df["数量"].isna().sum() - qty_na_before#to_numeric转换后空值的部分减去转换前的空值部分，说明提取失败
    report["单价提取失败"] = df["单价(元)"].isna().sum() - price_na_before

    # ---------- 6. 填充缺失值 ----------
    for col in ["数量", "单价(元)"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    report["最终行数"] = len(df)
    report["最终列数"] = len(df.columns)

    # ==================== F3：打印清洗报告 ====================
    print("\n")
    print("数据清洗报告 (F3)")
    print("=" * 50)
    print(f"【原始数据】{report['原始行数']} 行 × {report['原始列数']} 列")
    print(f"【删除全空行】{report['删除全空行']} 行（整行都是空值）")
    print(f"【删除重复行】{report['删除重复行']} 行（完全相同的行）")
    print(f"【日期字段】")
    print(f"   · 格式错误（如 2026-13-45）：{report['日期格式错误']} 个 → 标记为“日期格式错误”")
    print(f"   · 原本缺失：{report['日期原本缺失']} 个 → 标记为“未知”")
    print(f"【数值字段】")
    print(f"   · 数量原本缺失：{report['数量原本缺失']} 个 → 填充为 0")
    print(f"   · 数量提取失败：{report['数量提取失败']} 个 → 填充为 0")
    print(f"   · 单价原本缺失：{report['单价原本缺失']} 个 → 填充为 0")
    print(f"   · 单价提取失败：{report['单价提取失败']} 个 → 填充为 0")
    print(f"【最终数据】{report['最终行数']} 行 × {report['最终列数']} 列")
    print("=" * 50)

    return df, report