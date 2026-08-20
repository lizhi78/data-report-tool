# 数据分析报告生成工具

自动完成脏数据读取、清洗统计、异常识别，调用 AI 生成业务分析，输出 Excel 结果与 Markdown 报告。

## 项目功能

- F1：读取 CSV / Excel 原始数据文件
- F2‑F3：数据清洗，处理空格、千分位、单位、缺失、重复，输出清洗日志
- F4：数据描述统计、分组汇总统计
- F5：识别并标记业务异常数据
- F6：调用大模型 API 自动生成业务分析文本
- F7：导出多 sheet 清洗结果 Excel
- F8：输出完整 Markdown 分析报告
- F9：命令行传参运行，不硬编码文件路径

## 环境部署

### 1. 获取项目

拿到完整项目文件夹，终端切换到项目根目录 `DATA‑REPORT‑TOOL`

### 2. 安装第三方依赖

```
pip install -r requirements.txt
```

### 3. 配置 API 密钥

根目录已存在 `.env` 文件，在里面填入自己的密钥

```
DEEPSEEK_API_KEY="填入你的密钥"
```

> 
> ⚠️ `.env` 已经配置在 `.gitignore`，**禁止提交到 git 仓库**，防止密钥泄露。

## 使用方式

### 命令行运行

```
python main.py --input 你的数据文件.csv --output ./output
```

参数说明

- `--input`：必填，原始脏数据路径，支持`.csv`、`.xlsx`
- `--output`：必填，输出文件存放目录，本项目默认使用`./output`

示例

```
python main.py --input ./data/实习练习‑销售脏数据.csv --output ./output
```

程序执行完毕，清洗后的 Excel、md 报告全部生成在 `output` 文件夹。



```
DATA‑REPORT‑TOOL/
├── output/            # 程序输出：清洗excel、md报告
├── .env               # API密钥配置，不上传git
├── .gitignore         # git忽略规则配置
├── ai_report.py       # F6：调用大模型，生成AI分析文本
├── analyzer.py        # F4 F5：统计计算、异常识别标记
├── cleaner.py         # F2 F3：数据清洗逻辑、清洗日志
├── config.py          # 读取环境变量、全局配置
├── exporter.py        # F7 F8：导出Excel、Markdown报告
├── loader.py          # F1：读取csv、excel原始数据
├── main.py            # 程序入口，命令行解析，调度各个模块
├── README.md          # 项目说明文档（本文件）
└── requirements.txt   # 第三方库依赖清单
```

