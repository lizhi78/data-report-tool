import re
import pandas as pd
from analyzer import abnormal_data

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


    '''
    这段代码绕远了，我已经有了原本缺失和日期格式错误的行数了，直接将二者相加即可得到总的解析失败行数
    #统计所有转换后还是空值的行数
    date_parse_failures_total = df["Date"].isna().sum()
    report["日期解析失败（总计）"] = date_parse_failures_total
    #计算解析成功的数量
    report["日期解析成功"] = len(df) - date_parse_failures_total
    '''

    # 清洗后还是空的 = 格式错误 + 原本就空
    date_still_nat = df["Date"].isna()#在进行to_datetime转换后，仍然是空值的部分
    report["日期格式错误"] = (date_still_nat & ~date_was_empty).sum()#之前不是空值，转换后变成空值的部分，说明格式错误

    # 直接相加，避免重复计算
    report["日期解析失败（总计）"] = report["日期格式错误"] + report["日期原本缺失"]
    # 计算解析成功的数量
    report["日期解析成功"] = len(df) - report["日期解析失败（总计）"]

    df["Date"] = df["Date"].astype(object)
    df.loc[date_still_nat & ~date_was_empty, "Date"] = "日期格式错误"   
    df.loc[date_still_nat & date_was_empty, "Date"] = "未知"

    # ---------- 5. 数值提取 ----------
    # 记录提取前有多少空值
    qty_na_before = df["数量"].isna().sum()
    report["数量原本缺失"] = qty_na_before
    price_na_before = df["单价(元)"].isna().sum()
    report["单价原本缺失"] = price_na_before


     #将数字之间的逗号、空格、货币符号去掉，方便后续转换成数值类型（如"1,000" → "1000"，"¥ 100" → "100"）,否则.str.extract(r'(\d+)')[0]会出现问题1，999会直接被转换成1
    df["数量"] = df["数量"].astype(str).str.replace(r'[,\s]', '', regex=True)
    df["单价(元)"] = df["单价(元)"].astype(str).str.replace(r'[,\s]', '', regex=True)
    df["单价(元)"] = df["单价(元)"].str.extract(r'(\d+\.?\d*)')[0]#使得单价(元)列可以提取小数点后的数字，避免被截断(虽然实际上并没有)

    df["数量"] = df["数量"].astype(str).str.extract(r'(\d+\.?\d*)')[0]#取 [0] 变成普通 Series，否则是一个DF
    df["数量"] = pd.to_numeric(df["数量"], errors="coerce")
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
    df_with_anomalies = abnormal_data(df.copy()) # 使用 copy 避免修改原始清洗后的 df

    # 统计结果中 "异常" 的数量
    # 创建一个布尔掩码，标记任意一列为"异常"的行
    anomaly_rows_mask = (
        (df_with_anomalies["数量"] == "异常") |
        (df_with_anomalies["单价(元)"] == "异常") |
        (df_with_anomalies["销售额"] == "异常")
    )
    total_anomaly_records = anomaly_rows_mask.sum()

    report["异常记录总数"] = total_anomaly_records

    # ==================== F3：打印清洗报告 ====================
    print("\n")
    print("数据清洗报告 (F3)")
    print("=" * 50)
    print(f"【原始数据】{report['原始行数']} 行 × {report['原始列数']} 列")
    print(f"【删除全空行】{report['删除全空行']} 行（整行都是空值）")
    print(f"【删除重复行】{report['删除重复行']} 行（完全相同的行）")
    print(f"【日期字段】")
    print(f"   · 解析成功：{report['日期解析成功']} 个")
    print(f"   · 解析失败（总计）：{report['日期解析失败（总计）']} 个")
    print(f"   · 格式错误（如 2026-13-45）：{report['日期格式错误']} 个 → 标记为“日期格式错误”")
    print(f"   · 原本缺失：{report['日期原本缺失']} 个 → 标记为“未知”")
    print(f"【数值字段】")
    print(f"   · 数量原本缺失：{report['数量原本缺失']} 个 → 填充为 0")
    print(f"   · 数量提取失败：{report['数量提取失败']} 个 → 填充为 0")
    print(f"   · 单价原本缺失：{report['单价原本缺失']} 个 → 填充为 0")
    print(f"   · 单价提取失败：{report['单价提取失败']} 个 → 填充为 0")
    print(f"【最终数据】{report['最终行数']} 行 × {report['最终列数']} 列")
    print(f"【异常记录总数】{report['异常记录总数']} 行（数量、单价或销售额为“异常”）")
    print("=" * 50)

    return df, report