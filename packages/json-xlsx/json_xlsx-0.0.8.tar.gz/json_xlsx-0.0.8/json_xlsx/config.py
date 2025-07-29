"""
转换器配置设置
"""

# 转换器配置
CONVERTER_CONFIG = {
    'max_depth': 10,  # 最大递归深度
    'separator': '/',  # 键名分隔符
    'array_format': 'formatted',  # 数组格式化方式: 'formatted' 或 'json'
    'auto_width': True,  # 自动调整列宽
    'wrap_text': True,  # 自动换行
    'max_column_width': 100,  # 最大列宽
    'min_column_width': 12,  # 最小列宽
    'row_height_factor': 15,  # 行高系数
    'header_background_color': '005BAC',  # 表头背景色
    'header_font_color': 'FFFFFF',  # 表头字体颜色
}

# Excel工作表配置
SHEET_CONFIG = {
    'flattened_sheet_name': 'data',
    'original_sheet_name': 'source',
    'index_column_name': 'index',
    'json_column_name': 'json',
}

# 数据验证配置
VALIDATION_CONFIG = {
    'max_records': 20000,  # 最大记录数
    'max_field_length': 32767,  # Excel单元格最大字符数
    'empty_data_handling': 'skip',  # 空数据处理: 'skip', 'error', 'warning'
}