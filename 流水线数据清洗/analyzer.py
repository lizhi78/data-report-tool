import pandas as pd


    # ---------- 异常数据处理 ----------
def abnormal_data(df):
    #备份销售额数据(销售额_previous)并使其生成在销售额旁边
    df["销售额_previous"]=df["销售额"].copy()
    #从头到尾就是对表头list进行操作(移除，插入，获取索引等)，只有最后一步df=df[cols]是对整个Dataframe进行操作
    cols=list(df.columns)#将表头转换成一个list，方便后续的移除，插入，获取索引等操作

    cols.remove("销售额_previous")
    sales_index=cols.index("销售额")
    cols.insert(sales_index+1,"销售额_previous")
    df=df[cols]

    异常行=(df["数量"]>1000)|(df["数量"]<=0)|(df["单价(元)"]<=0)

    df.loc[~异常行,"销售额"]=df.loc[~异常行,"数量"]*df.loc[~异常行,"单价(元)"]
    #~异常行是异常行取非操作也就是正常行
    df["数量"] = df["数量"].astype(object)
    df["单价(元)"] = df["单价(元)"].astype(object)
    df["销售额"] = df["销售额"].astype(object)



    df.loc[异常行,"数量"]="异常"
    df.loc[异常行,"单价(元)"]="异常"
    df.loc[异常行,"销售额"]="异常"
    return df


def statistic_data(df):
    # ---------- 1. 创建临时数字列 ----------
    #转换成float类型，方便后续的.describe()和groupby()计算
    df["销售额_数字"] = pd.to_numeric(df["销售额"], errors="coerce")
    df["数量_数字"] = pd.to_numeric(df["数量"], errors="coerce")
    df["单价_数字"] = pd.to_numeric(df["单价(元)"], errors="coerce")

    # ========== 新增：过滤掉月份里的脏数据 ==========

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")#转换成datetime类型，方便后续的月份统计
    正常月份 = df["Date"].notna()#获取bool类型的Series，True表示正常月份，False表示脏数据
    clean_table = df[正常月份].copy()
    # ==============================================

    # ---------- F4.1 描述性统计（用干净表）----------
    print("【描述性统计】")
    desc_stats = clean_table[["数量_数字", "单价_数字", "销售额_数字"]].describe()
    print(desc_stats)

    # ---------- F4.2 分组统计（都用 干净表）----------
    print("\n【按类别汇总】")
    stat_category = clean_table.groupby("类别")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_category.columns = ["类别", "销售额合计"]
    print(stat_category)

    print("\n【按地区汇总】")
    stat_region = clean_table.groupby("地区")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_region.columns = ["地区", "销售额合计"]
    print(stat_region)

    print("\n【按销售员汇总】")
    stat_sales = clean_table.groupby("销售员")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_sales.columns = ["销售员", "销售额合计"]
    print(stat_sales)

    print("\n【按月份汇总】")
    clean_table["月份"]=clean_table["Date"].dt.strftime("%Y-%m")#从日期里把"年份"和"月份"抽出来，中间加个横杠，拼成一个字符串。这样同一个年月的所有日期，都会变成一样的字符串，方便后续按月份分组统计。

    stat_month = clean_table.groupby("月份")["销售额_数字"].sum().sort_values(ascending=False).reset_index()
    stat_month.columns = ["月份", "销售额合计"]
    print(stat_month)


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
