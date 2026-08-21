import pandas as pd


def save_excel(df_final, stats_dict, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_final.to_excel(writer, sheet_name="清洗后数据", index=False)
        stats_dict["按类别汇总"].to_excel(writer, sheet_name="按类别汇总", index=False)
        stats_dict["按地区汇总"].to_excel(writer, sheet_name="按地区汇总", index=False)
        stats_dict["按销售员汇总"].to_excel(writer, sheet_name="按销售员汇总", index=False)
        stats_dict["按月份汇总"].to_excel(writer, sheet_name="按月份汇总", index=False)


def save_markdown(file_name, stats_dict, ai_analysis, output_path):
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(f"# {file_name} 数据分析报告\n\n")
        
        f.write("## AI 分析洞察\n\n")
        f.write(ai_analysis)
        f.write("\n\n---\n\n")
        
        # 直接遍历4个汇总表，to_markdown() 一键转表格
        for name, df in stats_dict.items():
            f.write(f"## {name}\n\n")
            f.write(df.to_markdown(index=False))
            f.write("\n\n")

