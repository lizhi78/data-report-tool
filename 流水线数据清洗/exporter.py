import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


def save_excel(df_final, stats_dict, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_final.to_excel(writer, sheet_name="清洗后数据", index=False)
        stats_dict["按类别汇总"].to_excel(writer, sheet_name="按类别汇总", index=False)
        stats_dict["按地区汇总"].to_excel(writer, sheet_name="按地区汇总", index=False)
        stats_dict["按销售员汇总"].to_excel(writer, sheet_name="按销售员汇总", index=False)
        stats_dict["按月份汇总"].to_excel(writer, sheet_name="按月份汇总", index=False)


def save_markdown(file_name, stats_dict, ai_analysis, output_path):
    output_dir = os.path.dirname(output_path) or "."
    category_data = stats_dict.get("按类别汇总", pd.DataFrame())
    
    chart_path = None
    if not category_data.empty and "类别" in category_data.columns and "销售额合计" in category_data.columns:
        plt.figure(figsize=(8, 5))
        plt.bar(category_data["类别"], category_data["销售额合计"])
        plt.title("按类别销售额")
        plt.xlabel("类别")
        plt.ylabel("销售额合计")
        plt.xticks(rotation=45)
        plt.yscale('log')
        plt.tight_layout()
        
        chart_path = os.path.join(output_dir, f"{file_name}_chart.png")
        plt.savefig(chart_path)
        plt.close()
    
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(f"# {file_name} 数据分析报告\n\n")
        
        if chart_path:
            f.write("## 按类别销售额\n\n")
            f.write(f"![柱状图]({os.path.basename(chart_path)})\n\n")
        
        f.write("## AI 分析洞察\n\n")
        f.write(ai_analysis)
        f.write("\n\n---\n\n")
        
        for name, df in stats_dict.items():
            f.write(f"## {name}\n\n")
            f.write(df.to_markdown(index=False))
            f.write("\n\n")