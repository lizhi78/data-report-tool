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

#11. 写一个函数 算销售额(订单)，传入一条订单，返回销售额。
#    然后用它重做第 3 题。
def 销售额 (lista):
    total=lista["数量"]*lista["单价"]
    return total
a=销售数据[0]
price=销售额(a)
print(f"第一条订单的销售额是{price}")
# 12. 写一个函数 地区总额(数据, 地区名)，返回该地区的销售额合计。
#     用它算出「华东」的总额。
def 销售额 (lista):
    total=lista["数量"]*lista["单价"]
    return total
def addresstotal(数据,地区名):
    addresstotal_num=0  
    for one in 数据 :
        if one["地区"]==地区名:
            addresstotal_num += 销售额(one)
    return addresstotal_num

area=input("请输入地区是：")
money=addresstotal(销售数据,area)
print(f"{area}地区的销售额总计是{money}")
#13. 算出所有订单的总销售额、平均销售额、最大单笔销售额。
#    平均值保留 2 位小数
def biggest_sales(list):
    most_expensive_order = 销售数据[0]
    for b in 销售数据:
        if b["单价"]>most_expensive_order["单价"]:
            most_expensive_order=b 
    return most_expensive_order["单价"]
total_sales=0
for data in 销售数据:
    sales=销售额(data)
    total_sales+=sales
average_sales=round(total_sales/len(销售数据),2)
biggestsales=biggest_sales(data)
print(f"所有订单的销售总额是{total_sales},平均销售额是{average_sales:.2f},最大单笔销售额是{biggestsales}")
'''
14. ★ 按地区分组统计销售额，打印每个地区的总额，像这样：
      华东: 26372
      华北: 7676
      华南: 9896
      西南: 3915

      提示：建一个空字典，循环时判断地区在不在字典里，
      不在就新建、在就累加。
      这题写完记一下你写了多少行——周二用 pandas 一行就能做完。

area_dic={}
for list in 销售数据:
    sales=销售额(list)
    if list["地区"] not in area_dic:
        area_dic[list["地区"]]=sales
    else:
        area_dic[list["地区"]]+=sales
for area,sale in area_dic.items():
    print(f"{area}:{sale}")
'''
#pandas的写法
def 销售额 (lista):
    total=lista["数量"]*lista["单价"]
    return total
import pandas as pd
df = pd.DataFrame(销售数据)
df["销售额"] = 销售额(df)
print(df.groupby("地区")["销售额"].sum())


#15. 按「类别」分组，统计每个类别的订单数和总销售额。
catagory_dict={}
for lista in 销售数据:
    a_sale=销售额(lista)
    catagory=lista["类别"]
    if catagory not in catagory_dict:
        catagory_dict[catagory]=[1,a_sale]
    else:
        catagory_dict[catagory][0]=catagory_dict[catagory][0]+1
        catagory_dict[catagory][1] = catagory_dict[catagory][1]+a_sale
for catagory,listb in catagory_dict.items():
    print(f"类别：{catagory},订单数量：{listb[0]},总销售额：{listb[1]}")
#category_dict = {类别名称: [订单总个数, 类别销售总额]}