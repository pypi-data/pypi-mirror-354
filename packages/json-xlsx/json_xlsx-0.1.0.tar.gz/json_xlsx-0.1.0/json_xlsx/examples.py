"""
示例数据
"""

from typing import List, Dict, Any


def get_sample_data() -> List[Dict[str, Any]]:
    """
    获取示例数据用于测试
    
    Returns:
        示例数据列表
    """
    
    return [
        {
            "id": 1,
            "name": "张三",
            "age": 30,
            "email": "zhangsan@example.com",
            "address": {
                "country": "中国",
                "province": "北京市",
                "city": "北京市",
                "district": "海淀区",
                "street": "中关村大街1号"
            },
            "skills": ["Python", "JavaScript", "SQL"],
            "work_experience": [
                {
                    "company": "科技公司A",
                    "position": "软件工程师",
                    "duration": "2020-2023",
                    "responsibilities": ["前端开发", "后端开发", "数据库设计"]
                },
                {
                    "company": "科技公司B", 
                    "position": "高级工程师",
                    "duration": "2023-至今",
                    "responsibilities": ["系统架构", "团队管理"]
                }
            ],
            "education": {
                "degree": "本科",
                "major": "计算机科学",
                "university": "清华大学",
                "graduation_year": 2020
            },
            "active": True,
            "salary": 25000.50
        },
        {
            "id": 2,
            "name": "李四",
            "age": 28,
            "email": "lisi@example.com",
            "address": {
                "country": "中国",
                "province": "上海市",
                "city": "上海市",
                "district": "浦东新区",
                "street": "陆家嘴金融街99号"
            },
            "skills": ["Java", "Spring", "MySQL", "Redis"],
            "work_experience": [
                {
                    "company": "金融科技公司",
                    "position": "后端工程师",
                    "duration": "2021-至今",
                    "responsibilities": ["API开发", "微服务架构", "性能优化"]
                }
            ],
            "education": {
                "degree": "硕士",
                "major": "软件工程",
                "university": "复旦大学",
                "graduation_year": 2021
            },
            "active": True,
            "salary": 30000.00
        },
        {
            "id": 3,
            "name": "王五",
            "age": 35,
            "email": "wangwu@example.com",
            "address": {
                "country": "中国",
                "province": "广东省",
                "city": "深圳市",
                "district": "南山区",
                "street": "科技园南路100号"
            },
            "skills": ["React", "Vue.js", "Node.js", "TypeScript", "Docker"],
            "work_experience": [
                {
                    "company": "互联网公司C",
                    "position": "前端负责人",
                    "duration": "2018-2022",
                    "responsibilities": ["前端架构", "团队管理", "技术选型"]
                },
                {
                    "company": "创业公司D",
                    "position": "技术总监",
                    "duration": "2022-至今",
                    "responsibilities": ["技术管理", "产品规划", "团队建设"]
                }
            ],
            "education": {
                "degree": "本科",
                "major": "软件工程",
                "university": "华南理工大学",
                "graduation_year": 2018
            },
            "active": False,
            "salary": 45000.00
        }
    ]


def get_sample_contracts() -> List[Dict[str, Any]]:
    """
    获取复杂合同示例数据（简化版）
    
    Returns:
        合同数据列表
    """
    
    return [
        {
            "合同编号": "CONTRACT-2025-IT-001",
            "合同名称": "企业数字化转型系统开发项目",
            "合同类型": "技术开发合同",
            "签署日期": "2025-06-01",
            "生效日期": "2025-06-15",
            "到期日期": "2026-12-31",
            "合同状态": "执行中",
            "合同金额": {
                "总金额": 2800000.00,
                "币种": "人民币",
                "税率": 0.06,
                "税额": 168000.00,
                "含税总额": 2968000.00
            },
            "甲方信息": {
                "公司名称": "北京创新科技集团有限公司",
                "统一社会信用代码": "91110000123456789A",
                "法定代表人": {
                    "姓名": "张强",
                    "身份证号": "110101198501011234",
                    "联系电话": "13800138001"
                },
                "注册地址": {
                    "省份": "北京市",
                    "城市": "北京市",
                    "区县": "海淀区",
                    "详细地址": "中关村科技园区创新大厦15层",
                    "邮政编码": "100080"
                }
            },
            "乙方信息": {
                "公司名称": "上海智慧软件开发有限公司",
                "统一社会信用代码": "91310000987654321B",
                "法定代表人": {
                    "姓名": "李明",
                    "身份证号": "310101198703051234",
                    "联系电话": "13900139001"
                }
            },
            "项目详情": {
                "项目背景": "甲方需要建设全面的数字化转型平台，提升企业运营效率",
                "项目目标": [
                    "建立统一的数据管理平台",
                    "实现业务流程数字化",
                    "提升决策分析能力",
                    "降低运营成本20%以上"
                ],
                "交付物": [
                    {
                        "名称": "需求分析报告",
                        "描述": "详细的业务需求和技术需求分析文档",
                        "交付时间": "2025-07-15",
                        "责任人": "李明"
                    },
                    {
                        "名称": "系统架构设计",
                        "描述": "包含技术架构、数据架构、应用架构的设计文档",
                        "交付时间": "2025-08-30",
                        "责任人": "王技术"
                    }
                ]
            },
            "付款条款": {
                "付款方式": "分期付款",
                "付款计划": [
                    {
                        "阶段": "合同签署",
                        "付款比例": 0.20,
                        "付款金额": 560000.00,
                        "预期付款日期": "2025-06-15",
                        "状态": "已支付"
                    },
                    {
                        "阶段": "需求确认完成",
                        "付款比例": 0.15,
                        "付款金额": 420000.00,
                        "预期付款日期": "2025-07-22",
                        "状态": "待支付"
                    }
                ]
            }
        }
    ]