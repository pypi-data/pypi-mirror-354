# Excel Split Zim

一个简单的Python工具，用于将Excel文件按工作表拆分成多个独立的Excel文件。

## 安装

```bash
pip install excel_split_zim
```

## 使用方法

```python
from excel_split_zim import split_excel

# 拆分Excel文件
split_excel("path/to/your/excel/file.xlsx")
```

## 功能特点

- 自动将Excel文件中的每个工作表保存为独立的Excel文件
- 保持原始格式和样式
- 输出文件保存在原文件所在目录
- 简单易用的API

## 要求

- Python 3.6+
- openpyxl 3.0.0+

## 许可证

MIT License 