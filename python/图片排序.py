import os
import csv
import time

# 配置路径，改成你要遍历的文件夹路径
folder_path = "./img"
# 图片后缀
img_suffix = (".jpg", ".png", ".jpeg", ".bmp", ".gif")
file_list = []

# 1. os.walk遍历所有文件夹、子文件夹
for root, dirs, files in os.walk(folder_path):
    for name in files:
        # 判断是否是图片
        if name.lower().endswith(img_suffix):
            full_path = os.path.join(root, name)
            # 获取文件大小
            size = os.path.getsize(full_path)
            # 获取文件修改时间戳
            modify_ts = os.path.getmtime(full_path)
            # 时间戳转可读时间字符串
            modify_time = time.asctime(time.localtime(modify_ts))
            # 存入列表：文件名，大小，修改时间，修改时间戳（用来排序）
            file_list.append([name, size, modify_time, modify_ts])

# 定义函数：接收一行图片数据，返回下标3的时间戳
def get_sort_val(item):
    return item[3]

# 对图片列表进行排序
file_list.sort(key=get_sort_val, reverse=False)

# 3. 写入csv，去掉排序用的时间戳，只保留需要的三列
with open("图片清单.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    # 表头
    writer.writerow(["文件名", "文件大小(字节)", "修改时间"])
    for item in file_list:
        writer.writerow([item[0], item[1], item[2]])