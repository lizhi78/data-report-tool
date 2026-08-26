from pathlib import Path
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
    output_dir = Path(output_path).parent          # Path 提取文件所在文件夹
    category_data = stats_dict.get("按类别汇总", pd.DataFrame())
    
    chart_path = None
    if not category_data.empty and "类别" in category_data.columns and "销售额合计" in category_data.columns:
        plt.figure(figsize=(8, 5))               # 新建画布，宽8高5（英寸）
        plt.bar(category_data["类别"], category_data["销售额合计"])  # 画柱状图：x=类别，y=销售额
        plt.title("按类别销售额")                 # 图表标题
        plt.xlabel("类别")                       # 横轴标签
        plt.ylabel("销售额合计")                  # 纵轴标签
        plt.xticks(rotation=45)                  # x轴文字旋转45°，防重叠
        plt.yscale('log')                        # 纵轴改对数刻度，小数也能看清
        plt.tight_layout()                       # 自动调整边距，防止文字被裁
        
        chart_path = output_dir / f"{file_name}_chart.png"  # Path 用 / 拼接路径，自动适配系统
        plt.savefig(chart_path)                  # 保存图片到上述路径
        plt.close()                              # 关闭画布，释放内存
    
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(f"# {file_name} 数据分析报告\n\n")
        
        if chart_path:
            f.write("## 按类别销售额\n\n")
            f.write(f"![柱状图]({chart_path.name})\n\n")  # chart_path.name 取文件名（不含文件夹）
        #[柱状图](a.png)    柱状图  普通链接，点击后打开图片文件；[柱状图](a.png)	直接显示图片	嵌入图片，在文档里直接看到图

        f.write("## AI 分析洞察\n\n")
        f.write(ai_analysis)
        f.write("\n\n---\n\n")
        
        for name, df in stats_dict.items():
            f.write(f"## {name}\n\n")
            f.write(df.to_markdown(index=False))
            f.write("\n\n")