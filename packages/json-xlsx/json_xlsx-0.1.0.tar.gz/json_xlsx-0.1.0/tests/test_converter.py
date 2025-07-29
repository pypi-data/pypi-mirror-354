"""
JSON转Excel转换器测试
"""
from json_xlsx import JsonToExcelConverter, convert_json_to_excel
from json_xlsx.examples import get_sample_data, get_sample_contracts
import unittest
import tempfile
import os
from pathlib import Path

# 添加父目录到路径以便导入
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestJsonToExcelConverter(unittest.TestCase):
    """测试转换器功能"""

    def setUp(self):
        """设置测试环境"""
        self.converter = JsonToExcelConverter()
        self.temp_dir = tempfile.mkdtemp()
        self.sample_data = get_sample_data()
        
    def tearDown(self):
        """清理测试环境"""
        # 清理临时文件
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_basic_conversion(self):
        """测试基本转换功能"""
        output_path = os.path.join(self.temp_dir, "test_basic.xlsx")
        
        result = self.converter.convert_to_excel(
            self.sample_data, 
            output_path, 
            verbose=False
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["records_count"], len(self.sample_data))
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(result["flattened_columns"], 10)

    def test_single_record_conversion(self):
        """测试单条记录转换"""
        output_path = os.path.join(self.temp_dir, "test_single.xlsx")
        single_record = self.sample_data[0]
        
        result = self.converter.convert_to_excel(
            [single_record], 
            output_path, 
            verbose=False
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["records_count"], 1)
        self.assertTrue(os.path.exists(output_path))

    def test_flatten_dict_functionality(self):
        """测试字典扁平化功能"""
        test_dict = {
            "name": "测试",
            "nested": {
                "level1": {
                    "level2": "深层值"
                }
            },
            "array": [1, 2, 3]
        }
        
        flattened = self.converter.flatten_dict(test_dict)
        
        self.assertIn("name", flattened)
        self.assertIn("nested/level1/level2", flattened)
        self.assertIn("array", flattened)
        self.assertEqual(flattened["nested/level1/level2"], "深层值")

    def test_complex_data_conversion(self):
        """测试复杂数据转换"""
        output_path = os.path.join(self.temp_dir, "test_complex.xlsx")
        complex_data = get_sample_contracts()
        
        result = self.converter.convert_to_excel(
            complex_data, 
            output_path, 
            verbose=False
        )
        
        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(result["flattened_columns"], 20)

    def test_custom_config(self):
        """测试自定义配置"""
        custom_config = {
            "separator": "_",
            "max_depth": 3
        }
        
        converter = JsonToExcelConverter(custom_config)
        self.assertEqual(converter.config["separator"], "_")
        self.assertEqual(converter.config["max_depth"], 3)

    def test_simplified_api(self):
        """测试简化API"""
        output_path = os.path.join(self.temp_dir, "test_api.xlsx")
        
        # 测试列表输入
        result = convert_json_to_excel(self.sample_data, output_path)
        self.assertTrue(result["success"])
        
        # 测试单个字典输入
        output_path2 = os.path.join(self.temp_dir, "test_api_single.xlsx")
        result2 = convert_json_to_excel(self.sample_data[0], output_path2)
        self.assertTrue(result2["success"])

    def test_error_handling(self):
        """测试错误处理"""
        output_path = os.path.join(self.temp_dir, "test_error.xlsx")
        
        # 测试空数据
        result = self.converter.convert_to_excel([], output_path, verbose=False)
        self.assertFalse(result["success"])
        
        # 测试无效路径
        invalid_path = "/invalid/path/test.xlsx"
        result = self.converter.convert_to_excel(
            self.sample_data, 
            invalid_path, 
            verbose=False
        )
        self.assertFalse(result["success"])

    def test_converter_instance_methods(self):
        """测试转换器实例方法"""
        output_path = os.path.join(self.temp_dir, "test_instance.xlsx")
        
        # 测试convert方法（简化接口）
        result = self.converter.convert(
            self.sample_data[0],  # 单个字典
            output_path,
            verbose=False
        )
        
        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(output_path))


class TestDataFormatters(unittest.TestCase):
    """测试数据格式化器"""
    
    def test_array_formatting(self):
        """测试数组格式化"""
        from json_xlsx.formatters import CellFormatter
        
        # 测试简单数组
        simple_array = [1, 2, 3]
        formatted = CellFormatter.format_value(simple_array)
        self.assertEqual(formatted, "1, 2, 3")
        
        # 测试对象数组
        object_array = [
            {"name": "张三", "age": 30},
            {"name": "李四", "age": 25}
        ]
        formatted = CellFormatter.format_value(object_array)
        self.assertIn("[1]", formatted)
        self.assertIn("张三", formatted)
        
        # 测试布尔值
        self.assertEqual(CellFormatter.format_value(True), "是")
        self.assertEqual(CellFormatter.format_value(False), "否")
        
        # 测试None值
        self.assertEqual(CellFormatter.format_value(None), "")


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)