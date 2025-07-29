"""
数据格式化组件
"""

import json
from typing import Any, List, Dict, Union
from .config import VALIDATION_CONFIG


class ArrayFormatter:
    """数组数据格式化器"""

    @staticmethod
    def format_object_array(arr: List[Dict[str, Any]]) -> str:
        """
        格式化对象数组为可读字符串

        Args:
            arr: 对象数组

        Returns:
            格式化后的字符串
        """
        if not arr:
            return ""

        lines = []
        for i, item in enumerate(arr, 1):
            if isinstance(item, dict):
                pairs = []
                for k, v in item.items():
                    # 处理嵌套值
                    if isinstance(v, (dict, list)):
                        v_str = json.dumps(v, ensure_ascii=False)
                        # 限制嵌套内容长度，避免过长
                        if len(v_str) > 20000:
                            v_str = v_str[:97] + "..."
                    else:
                        v_str = str(v)
                    pairs.append(f"{k}: {v_str}")
                lines.append(f"[{i}] {', '.join(pairs)}")
            else:
                lines.append(f"[{i}] {str(item)}")

        return "\n".join(lines)

    @staticmethod
    def format_mixed_array(arr: List[Any]) -> str:
        """
        格式化混合类型数组

        Args:
            arr: 混合类型数组

        Returns:
            格式化后的字符串
        """
        if not arr:
            return ""

        # 检查数组类型
        has_objects = any(isinstance(item, dict) for item in arr)

        if has_objects:
            return ArrayFormatter.format_object_array(arr)
        else:
            # 简单类型数组，用逗号分隔
            return "\n".join(str(item) for item in arr)


class CellFormatter:
    """单元格格式化器"""

    @staticmethod
    def format_value(value: Any) -> Union[str, Any]:
        """
        格式化单元格值

        Args:
            value: 原始值

        Returns:
            格式化后的值
        """
        if value is None:
            return ""

        if isinstance(value, list):
            if not value:
                return ""
            elif all(isinstance(item, dict) for item in value):
                return ArrayFormatter.format_object_array(value)
            else:
                return ArrayFormatter.format_mixed_array(value)

        elif isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False, indent=2)

        elif isinstance(value, bool):
            return "是" if value else "否"

        elif isinstance(value, (int, float)):
            return value

        else:
            # 字符串类型，检查长度
            str_value = str(value)
            max_length = VALIDATION_CONFIG.get("max_field_length", 32767)
            if len(str_value) > max_length:
                return str_value[: max_length - 3] + "..."
            return str_value