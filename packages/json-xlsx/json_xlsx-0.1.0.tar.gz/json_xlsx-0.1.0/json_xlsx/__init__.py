"""
JSON转Excel转换器 - 简单易用的Python库

将复杂的嵌套JSON数据转换为格式化的Excel文件

用法示例:
    from json_xlsx import JsonToExcelConverter
    
    converter = JsonToExcelConverter()
    result = converter.convert(data, "output.xlsx")
"""

__version__ = "0.1.0"
__author__ = "Quant"
__email__ = "pengzhia@gmail.com"
__description__ = "Convert nested JSON data to formatted Excel files"

from .converter import JsonToExcelConverter
from .config import CONVERTER_CONFIG, VALIDATION_CONFIG


# 简化的API
def convert_json_to_excel(data, output_path, config=None):
    """
    简化的转换函数
    
    Args:
        data: JSON数据列表或单个字典
        output_path: 输出Excel文件路径
        config: 可选配置字典
    
    Returns:
        转换结果字典
    """
    converter = JsonToExcelConverter(config)
    
    # 如果输入是单个字典，转换为列表
    if isinstance(data, dict):
        data = [data]
    
    return converter.convert_to_excel(data, output_path)

def merge_sheets(excel_files, output_path):
    """
    合并多个Excel文件
    """
    converter = JsonToExcelConverter()
    return converter.merge_excel_files(excel_files, output_path)

# 导出主要组件
__all__ = [
    "JsonToExcelConverter",
    "convert_json_to_excel",
    "merge_sheets",
    "CONVERTER_CONFIG",
    "VALIDATION_CONFIG"
]