# 导入os系统模块：实现文件夹判断、路径拼接、递归遍历文件夹
import os
# 导入csv模块：用于把统计结果写入CSV表格，可用Excel/WPS直接打开
import csv
# 导入string字符串工具模块：快速获取全部英文标点符号
import string
# 导入jieba第三方分词库：对中文句子进行词语切割，需要提前执行pip install jieba安装
import jieba
# 从Python内置集合工具库导入Counter计数器，专门用来统计词语出现频次
from collections import Counter

# 配置参数1：需要批量扫描txt文件的文件夹路径（相对路径，和代码放在同一个文件夹）
path = r"C:\Users\wutia\Desktop\统计字数"
# 配置参数2：每个文本提取出现频次最高的前N个关键词，这里设定为前5个
top_num = 5

# 定义文本清洗函数
# 功能：去除原文中英文标点、中文标点、纯数字、空格换行空白符，只保留纯汉字
def clean(txt):
    # 将英文标点字符串转为集合，集合做字符匹配查询速度更快
    en_punc = set(string.punctuation)
    # 手动定义常用中文标点集合，Python没有内置中文标点集合，需要手动列举
    cn_punc = {"，", "。", "、", "；", "：", "？", "！", "“", "”", "‘", "’", "《", "》", "……", "——", "（", "）"}
    # 集合运算符 | 合并两个标点集合，整合所有中英文标点
    all_punc = en_punc | cn_punc
    # 定义空字符串，用来存放过滤完成后的纯净汉字文本
    res = ""
    # 循环遍历原始文本的每一个单独字符
    for c in txt:
        # 判断条件：字符不属于标点 并且 不是数字 并且 不是空格/换行等空白字符
        if c not in all_punc and not c.isdigit() and not c.isspace():
            # 满足条件的汉字拼接进结果字符串
            res += c
    # 返回清洗完毕的纯汉字文本
    return res

# 定义词频统计函数
# 入参：txt原始文本，n需要提取的高频词数量
# 返回值：文章有效汉字总长度、排序后的高频词列表（词语，出现次数）
def word_stat(txt, n):
    # 调用清洗函数，对原始文本进行去污处理
    clean_txt = clean(txt)
    # 纯净文本的字符长度 = 文章有效汉字总字数
    length = len(clean_txt)
    # jieba.lcut精准模式分词，把一整段中文切分为独立词语，返回词语列表
    word_list = jieba.lcut(clean_txt)
    # 列表推导式过滤分词结果，只保留2个字及以上词语，过滤“的、了、很”这类无意义单字
    word_filter = [w for w in word_list if len(w)>=2]
    # 使用Counter对过滤后的词语列表做频次统计，自动记录每个词语出现多少次
    count = Counter(word_filter)
    # most_common(n)：将词语按照出现次数从高到低排序，截取前n个高频关键词
    hot = count.most_common(n)
    # 同时返回两个结果：有效字数、高频词数据
    return length, hot

# 主业务执行函数：文件夹遍历、文件读取、文本统计、控制台输出、表格导出
def run(folder):
    # 判断目标文件夹是否真实存在
    if not os.path.exists(folder):
        # 文件夹不存在，控制台提示文字
        print("文件夹不存在")
        # 直接结束主函数，不再向下执行
        return
    # 二维列表，用来存储所有txt文件的最终统计结果，一行对应一个文件数据
    out = []
    # 定义计数器，统计程序一共找到多少个TXT文件
    count_file = 0

    # os.walk递归遍历文件夹，自动遍历当前文件夹以及所有嵌套的子文件夹
    # root：当前遍历到的文件夹完整路径
    # dirs：当前文件夹内部所有子文件夹名称列表
    # files：当前文件夹内部所有文件名称列表
    for root, dirs, files in os.walk(folder):
        # 循环遍历当前文件夹内每一个文件
        for name in files:
            # name.lower()将文件名全部转为小写，兼容.TXT大写后缀的文本文件
            if name.lower().endswith(".txt"):
                # 有效txt文件数量+1
                count_file += 1
                # 文件夹路径 + 文件名拼接成文件绝对路径，只有完整路径才能打开文件
                full_path = os.path.join(root, name)
                # try-except异常捕获，解决txt两种编码格式导致的中文乱码、程序崩溃问题
                try:
                    # 优先使用utf-8通用编码打开文件，只读模式读取全部文本内容
                    with open(full_path, "r", encoding="utf-8-sig") as f:
                        text = f.read()
                except:
                    # utf-8解码失败时，切换为GBK编码（Windows记事本默认保存编码）读取文件
                    with open(full_path, "r", encoding="gbk") as f:
                        text = f.read()
                # 调用词频统计函数，获取当前文件总字数、高频词原始数据
                char_len, hot_words = word_stat(text, top_num)
                # 遍历高频词元组，拼接为易读字符串格式：词语(次数)、词语(次数)
                hot_str = "、".join([f"{w}({num}次)" for w, num in hot_words])

                # 1. 准备空列表
                temp_list = []
                # 2. 循环遍历高频词
                for w, num in hot_words:
                    # 格式化文字
                    word_text = f"{w}({num}次)"
                    # 加入临时列表
                    temp_list.append(word_text)
                # 3. 顿号拼接成完整字符串
                hot_str = "、".join(temp_list)
                # 将单个文件的【文件名、总字数、格式化高频词】存入总结果列表
                out.append([name, char_len, hot_str])
                
    # 遍历完成后，如果没有找到任何txt文件
    if count_file == 0:
        # 控制台提示
        print("未找到任何txt文件")
        # 终止函数运行
        return

    # 控制台打印txt文件总数量，无分割线、对齐等美化格式
    print(f"总共扫描到 {count_file} 个txt文件")
    # 直接打印表格表头，无排版美化
    print("文件名 总字数 高频词")
    # 循环遍历所有文件结果，直接打印原始数据
    for line in out:
        print(line[0], line[1], line[2])

    # ===================== CSV表格写入 详细注释 =====================
    # with上下文管理器打开CSV文件，代码块执行结束自动关闭文件，避免文件占用锁定
    # "结果.csv" 生成的表格文件名，保存在代码同级目录
    # "w" 写入模式：文件不存在则新建，文件存在则清空原有内容重新写入
    # encoding="utf-8-sig" 特殊编码，解决Excel打开CSV中文乱码问题
    # newline="" 消除Windows系统下CSV自动产生的多余空白行
    with open("结果.csv", "w", encoding="utf-8-sig", newline="") as f:
        # 基于打开的文件对象，创建csv专用写入器，用来格式化写入表格内容
        w = csv.writer(f)
        # writerow：写入单行数据，写入表格第一行表头，列表内每个元素对应一列标题
        w.writerow(["文件名", "总文字数", f"前{top_num}高频词"])
        # writerows：批量写入多行数据，直接把二维列表out全部转为表格行，无需循环
        w.writerows(out)
    # 控制台提示用户表格导出完成
    print("数据已导出：结果.csv")

## Python程序入口判断
## 如果该文件被其他Python代码导入调用，不会自动运行主逻辑，防止误执行
if __name__ == "__main__":
    # 启动文本统计程序，传入配置好的文件夹路径
    run(path)