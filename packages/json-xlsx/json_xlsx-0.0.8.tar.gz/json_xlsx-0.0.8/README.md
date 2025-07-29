# json_xlsx

[![PyPI version](https://badge.fury.io/py/json_xlsx.svg)](https://badge.fury.io/py/json_xlsx)
[![Python versions](https://img.shields.io/pypi/pyversions/json_xlsx.svg "3.8")](https://pypi.org/project/json_xlsx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个简单易用的Python库，用于将复杂的嵌套JSON数据转换为格式化的Excel文件。

## ✨ 特性

* 🚀  **简单易用** : 一行代码完成JSON到Excel的转换
* 📊  **智能扁平化** : 自动处理深层嵌套的JSON结构
* 🎨  **精美格式** : 自动应用专业的Excel格式和样式
* 📋  **多工作表** : 同时生成原始数据和扁平化数据两个工作表
* 🔧  **高度可配置** : 支持自定义分隔符、深度限制等配置
* 📱  **数组友好** : 智能处理各种类型的数组数据
* 🌍  **中文支持** : 完美支持中文字符和内容

## 📦 安装

```bash
pip install json-xlsx
```

## 🚀 快速开始

### 快速体验

```python
"""
测试json_xlsx库
"""

import requests
from json_xlsx import convert_json_to_excel

# 获取响应数据
response = requests.get("https://dummyjson.com/recipes", timeout=10)
response_data = response.json()

# 获取第一个key的值
json_data = response_data.get(list(response_data.keys())[0])

# 配置表头背景色和字体颜色
CONFIG = {"header_background_color": "123456", "header_font_color": "FFFFFF"}

# 输出路径
OUTPUT_PATH = "sample.xlsx" 

# 转换数据
result = convert_json_to_excel(json_data, OUTPUT_PATH, CONFIG)

# 打印输出路径
print(result["output_path"])

```

### 基本用法

```python
from json_xlsx import convert_json_to_excel

# 准备JSON数据
data = [
    {
        "name": "张三",
        "age": 30,
        "address": {
            "city": "北京",
            "district": "海淀区"
        },
        "skills": ["Python", "JavaScript"]
    },
    {
        "name": "李四",
        "age": 25,
        "address": {
            "city": "上海", 
            "district": "浦东新区"
        },
        "skills": ["Java", "Spring"]
    }
]

# 转换为Excel
result = convert_json_to_excel(data, "output.xlsx")

if result["success"]:
    print(f"转换成功！生成了 {result['records_count']} 条记录")
else:
    print(f"转换失败: {result['error']}")
```

### 高级用法

```python
from json_xlsx import JsonToExcelConverter

# 自定义配置
config = {
    "separator": "_",           # 使用下划线作为字段分隔符
    "max_depth": 10,           # 最大递归深度
    "max_column_width": 80,    # 最大列宽
}

# 创建转换器
converter = JsonToExcelConverter(config)

# 执行转换
result = converter.convert(data, "advanced_output.xlsx")
```

## 📊 输出格式

转换后的Excel文件包含两个工作表：

1. **对比数据** : 扁平化后的结构化数据，便于分析和处理
2. **原始数据** : 保留原始JSON格式，便于追溯和查看

### 扁平化示例

输入JSON:

```json
{
    "user": {
        "name": "张三",
        "contact": {
            "email": "zhangsan@example.com"
        }
    }
}
```

扁平化结果:

| user/name | user/contact/email   |
| --------- | -------------------- |
| 张三      | zhangsan@example.com |

## ⚙️ 配置选项

```python
CONVERTER_CONFIG = {
    'max_depth': 15,              # 最大递归深度
    'separator': '/',             # 键名分隔符
    'auto_width': True,           # 自动调整列宽
    'wrap_text': True,            # 自动换行
    'max_column_width': 100,      # 最大列宽
    'min_column_width': 14,       # 最小列宽
    'row_height_factor': 18,      # 行高系数
    'header_background_color': '005BAC',  # 表头背景色
    'header_font_color': 'FFFFFF',  # 表头字体颜色
}
```

## 🔧 API 参考

### convert_json_to_excel(data, output_path, config=None)

简化的转换函数。

**参数:**

* `data`: JSON数据（列表或单个字典）
* `output_path`: 输出Excel文件路径
* `config`: 可选的配置字典

**返回:**
包含转换结果的字典

### JsonToExcelConverter

主要的转换器类。

**方法:**

* `__init__(config=None)`: 初始化转换器
* `convert(data, output_path, **kwargs)`: 简化的转换方法
* `convert_to_excel(data, output_path, verbose=True)`: 完整的转换方法
* `flatten_dict(data, parent_key="", sep=None, depth=0)`: 扁平化字典

## 📝 使用示例

### 处理复杂嵌套数据

```python
complex_data = {
    "company": "科技公司",
    "employees": [
        {
            "name": "张三",
            "position": "工程师",
            "skills": ["Python", "JavaScript"],
            "address": {
                "city": "北京",
                "district": "海淀区"
            }
        }
    ],
    "financial": {
        "revenue": 1000000,
        "expenses": {
            "salary": 600000,
            "rent": 120000
        }
    }
}

convert_json_to_excel(complex_data, "company_data.xlsx")
```

### 批量处理数据

```python
# 处理多条记录
records = [
    {"id": 1, "name": "产品A", "price": 99.99},
    {"id": 2, "name": "产品B", "price": 149.99},
    {"id": 3, "name": "产品C", "price": 199.99}
]

result = convert_json_to_excel(records, "products.xlsx")
print(f"处理了 {result['records_count']} 个产品")
```

## 🧪 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 运行示例
python examples/basic_usage.py
```

## 📋 系统要求

* Python 3.8+
* pandas >= 2.0.0
* openpyxl >= 3.0.0

## 📄 许可证

本项目采用 MIT 许可证。详情请查看 [LICENSE]() 文件。

## 🐛 问题反馈

如果您遇到任何问题或有功能建议，请在 [GitHub Issues](https://github.com/quantatirsk/json_xlsx/issues) 中提交。

## 📈 更新日志

### v0.0.8

* 支持嵌套JSON扁平化
* 自动Excel格式化
* 完整的测试覆盖
* 自定义标题行背景/字体颜色
