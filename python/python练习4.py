销售数据 = [
      {"订单号": "SO001", "日期": "2026-08-01", "产品": "笔记本电脑", "类别": "电脑整机", "数量": 2, "单价": 5999, "地区": "华东", "销售员": "张伟"},
      {"订单号": "SO002", "日期": "2026-08-01", "产品": "无线鼠标",   "类别": "外设",     "数量": 10, "单价": 89,   "地区": "华北", "销售员": "李娜"},
      {"订单号": "SO003", "日期": "2026-08-02", "产品": "机械键盘",   "类别": "外设",     "数量": 5,  "单价": 359,  "地区": "华东", "销售员": "王芳"},
      {"订单号": "SO004", "日期": "2026-08-02", "产品": "27寸显示器", "类别": "外设",     "数量": 3,  "单价": 1299, "地区": "华南", "销售员": "张伟"},
      {"订单号": "SO005", "日期": "2026-08-03", "产品": "蓝牙耳机",   "类别": "影音",     "数量": 8,  "单价": 499,  "地区": "华北", "销售员": "刘强"},
      {"订单号": "SO006", "日期": "2026-08-03", "产品": "U盘128G",    "类别": "存储",     "数量": 20, "单价": 79,   "地区": "西南", "销售员": "李娜"},
      {"订单号": "SO007", "日期": "2026-08-04", "产品": "移动硬盘2T", "类别": "存储",     "数量": 4,  "单价": 559,  "地区": "华东", "销售员": "陈静"},
      {"订单号": "SO008", "日期": "2026-08-04", "产品": "笔记本电脑", "类别": "电脑整机", "数量": 1,  "单价": 5999, "地区": "华南", "销售员": "王芳"},
      {"订单号": "SO009", "日期": "2026-08-05", "产品": "高清摄像头", "类别": "影音",     "数量": 6,  "单价": 299,  "地区": "华北", "销售员": "刘强"},
      {"订单号": "SO010", "日期": "2026-08-05", "产品": "无线鼠标",   "类别": "外设",     "数量": 15, "单价": 89,   "地区": "西南", "销售员": "陈静"},
  ]

#16. 把销售数据写进 销售数据.csv 文件（含表头）。
#     编码问题你上周注释过 utf-8-sig 是干嘛的，这里用上。
#     写完用 Excel 打开看看有没有乱码。
import csv
with open("销售数据.csv","w",encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=销售数据[0].keys())
    writer.writeheader()
    for data in 销售数据:
        writer.writerow(data)



#17. 从刚才那个 CSV 把数据读回来，打印前 3 条。
#    你会发现「数量」和「单价」变成字符串了，不能直接计算。想想为什么。

import csv

with open("销售数据.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    销售数据读回 = list(reader)
for i in range(3):
    print(销售数据读回[i])
#原因：CSV 文件本质是纯文本文件，不保存数据类型

#18. 把第 14 题的统计结果写成 JSON 文件 地区统计.json
#     注意 json.dump 要加 ensure_ascii=False，不然中文会变成一串 \u 编码。
import json
def 销售额 (lista):
    total=lista["数量"]*lista["单价"]
    return total
area_dic={}
for listb in 销售数据:
    sales=销售额(listb)
    if listb["地区"] not in area_dic:
        area_dic[listb["地区"]]=sales
    else:
        area_dic[listb["地区"]]+=sales
for area,sale in area_dic.items():
    print(f"{area}:{sale}")
with open("地区统计.json","w",encoding="utf-8-sig") as f:
    json.dump(area_dic,f,ensure_ascii=False)

'''
 19. ★ 写一个函数 转数字(值)，把下面这些都转成整数：

      "10"      →  10
      "  10 "   →  10      前后有空格
      "10个"    →  10      带单位
      "1,234"   →  1234    千分位逗号
      "5999元"  →  5999    带单位
      ""        →  0       空值
      "abc"     →  0       转不了的返回 0，不许崩

      提示：strip() 去空格、replace() 换掉逗号和单位、try/except 兜底。
      这题下周项目里直接要用。

def 转数字(值):
    s=值.strip( )
    s=s.replace(",","")
    s = s.replace("个","")
    s = s.replace("元","")
    try:
        return int(s)
    except:

    
    return 0
'''
#pandas写法
import pandas as pd
def 转数字(值):
    s=值.astype(str).str.strip()
    s = s.str.replace(",","")
    s = s.str.replace("个","")
    s = s.str.replace("元","")
    s=pd.to_numeric(s,errors="coerce").fillna("错误")
    return s




'''
 20. ★ 综合题：
      读第 16 题生成的 CSV → 用第 19 题的函数把数量单价转成数字
      → 按地区统计销售额 → 输出一份文本报告：

      === 销售分析报告 ===
      总订单数：10
      总销售额：47859

      各地区销售额：
        华东: 26372 (55.1%)
        华南: 9896 (20.7%)
        ...

      销售额最高的地区：华东
'''
with open("销售数据.csv","r",encoding="utf-8-sig") as f:
    reader=csv.DictReader(f)
    data=list(reader)


for row in data:
    row["数量"]=转数字(row["数量"])
    row["单价"]=转数字(row["单价"])

总订单数=len(data)

area_dict = {}
for row in data:
    area = row["地区"]
    money = row["数量"]*row["单价"]
    if area in area_dict:
        area_dict[area] = area_dict[area] + money
    else:
        area_dict[area] = money

总销售额=0
for area, money in area_dict.items():
    总销售额+=money

最高金额=0
最高地区=""   # 修复：提前定义变量
for area,money in area_dict.items():
    if money>最高金额:
        最高金额=money
        最高地区=area

print("=== 销售分析报告 ===")
print(f"总订单数：{总订单数}")
print(f"总销售额：{总销售额}")
print("\n")
print("各地区销售额：")
for area, money in area_dict.items():
    per=money/总销售额*100
    print(f"{area}: {money}({per:.1f}%)")
print("\n")
print(f"销售额最高的地区：{最高地区}")



