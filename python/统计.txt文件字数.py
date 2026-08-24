#读一个文件夹里所有 txt 文件，统计每个文件的字数
import os
path =r"C:\Users\wutia\Desktop\统计字数"
for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith(".txt"):
            path2=os.path.join(root,name)
            try:
                try:
                    with open (path2,"r",encoding="utf-8-sig") as f:
                        content=f.read()
                except:
                    with open (path2,"r",encoding="gbk") as f:
                        content=f.read()    
                total=len(content)
            except Exception as e:
                print(f"出现错误:{e}")
            else:
                print(f"文件是{path2}，该文件的字数是{total}")