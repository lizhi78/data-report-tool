import pandas as pd


def abnormal_data(df):
    # 备份销售额数据(销售额_previous)并使其生成在销售额旁边
    df["销售额_previous"]=df["销售额"].copy()
    # 从头到尾就是对表头list进行操作(移除，插入，获取索引等)，只有最后一步df=df[cols]是对整个Dataframe进行操作
    cols=list(df.columns)# 将表头转换成一个list，方便后续的移除，插入，获取索引等操作

    cols.remove("销售额_previous")
    sales_index = cols.index("销售额")
    cols.insert(sales_index + 1, "销售额_previous")
    df = df[cols]

    # 标记数量和单价的异常：小于等于0或大于9999
    数量异常_mask = (df["数量"] <= 0) | (df["数量"] > 9999)
    单价异常_mask = (df["单价(元)"] <= 0) | (df["单价(元)"] > 9999)
    
    # 计算初步的销售额（还未处理异常情况）
    calculated_sales = df["数量"] * df["单价(元)"]

    # 计算销售额校验：仅当重新计算的销售额与原销售额不一致时标记为异常
    销售额校验_bool = df["销售额_previous"] == calculated_sales
    # 将 bool 序列转换为"正常"/"异常"，并作为新列插入
    df["销售额校验"] = 销售额校验_bool.map({True: "原数据正常", False: "原数据异常"})
    
    # 调整列顺序，将销售额校验放在销售额_previous旁边
    cols = list(df.columns)
    cols.remove("销售额校验")
    previous_index = cols.index("销售额_previous")
    cols.insert(previous_index + 1, "销售额校验")
    df = df[cols]

    df["数量"] = df["数量"].astype(object)
    df["单价(元)"] = df["单价(元)"].astype(object)
    df["销售额"] = df["销售额"].astype(object)

    # 根据条件设置各列的值
    df.loc[数量异常_mask, "数量"] = "异常"
    df.loc[单价异常_mask, "单价(元)"] = "异常"
    
    # 销售额的逻辑：如果数量或单价有异常，则为“异常”，否则显示计算结果
    df.loc[数量异常_mask | 单价异常_mask, "销售额"] = "异常"
    df.loc[~(数量异常_mask | 单价异常_mask), "销售额"] = calculated_sales[~(数量异常_mask | 单价异常_mask)].values

    return df



def statistic_data(df):
    # ---------- 1. 创建临时数字列 ----------
    #转换成float类型，方便后续的.describe()和groupby()计算
    df["销售额_数字"] = pd.to_numeric(df["销售额"], errors="coerce")
    df["数量_数字"] = pd.to_numeric(df["数量"], errors="coerce")
    df["单价_数字"] = pd.to_numeric(df["单价(元)"], errors="coerce")

    # ---------- F4.2 分组统计（在完整表上进行，确保所有销售额都被计入，即使日期无效）----------
    print("\n【按类别汇总】")
    # 注意：这里使用的是 df，而不是 clean_table
    stat_category = df.groupby("类别")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_category.columns = ["类别", "销售额合计"]
    print(stat_category)

    print("\n【按地区汇总】")
    # 注意：这里使用的是 df
    stat_region = df.groupby("地区")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_region.columns = ["地区", "销售额合计"]
    print(stat_region)

    print("\n【按销售员汇总】")
    # 注意：这里使用的是 df
    stat_sales = df.groupby("销售员")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_sales.columns = ["销售员", "销售额合计"]
    print(stat_sales)

    # ========== 新增：过滤掉月份里的脏数据 ========== (必须在此处进行，因为 groupby 需要有效日期)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")#转换成datetime类型，方便后续的月份统计
    正常月份 = df["Date"].notna()#获取bool类型的Series，True表示正常月份，False表示脏数据
    clean_table = df[正常月份].copy()
    # ==============================================

    # ---------- F4.1 描述性统计（用干净表，因为描述性统计通常需要完整的数字列）----------
    print("【描述性统计】")
    # 这里使用 clean_table，因为无效日期行的 Date 列可能是 NaN，会影响 describe 的统计
    # 但更重要的是，如果这里的 "销售额_数字", "数量_数字", "单价_数字" 也有 NaN，
    # describe 会自动忽略它们，所以用 df 也是可以的，但用 clean_table 更明确。
    desc_stats = clean_table[["数量_数字", "单价_数字", "销售额_数字"]].describe()
    print(desc_stats)

    print("\n【按月份汇总】")
    # 按月份汇总必须依赖于有效的日期
    clean_table["月份"]=clean_table["Date"].dt.strftime("%Y-%m")

    stat_month = clean_table.groupby("月份")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_month.columns = ["月份", "销售额合计"]
    print(stat_month)

    # ... (收集 stats 字典和删除临时列的代码) ...


    # 5. 收集所有统计结果（返回给 main.py 保存）
    stats = {
        "描述性统计": desc_stats,
        "按类别汇总": stat_category,
        "按地区汇总": stat_region,
        "按销售员汇总": stat_sales,
        "按月份汇总": stat_month
    }

    # ---------- 3. 删除临时列 ----------
    df = df.drop(columns=["销售额_数字", "数量_数字", "单价_数字"])
    print("\n临时数字列已删除")

    df["Date"] = df["Date"].apply(lambda x: x.strftime("%Y-%m-%d") if pd.notna(x) else "")
    return df,stats