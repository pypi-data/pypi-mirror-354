import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.stata.session import StataSession


class TestStataSession(unittest.TestCase):
    """测试StataSession类的功能"""
    
    def setUp(self):
        """每个测试方法执行前的设置"""
        # 使用patch模拟_find_stata_installation方法，避免实际查找Stata路径
        self.find_stata_patcher = patch.object(StataSession, '_find_stata_installation', 
                                              return_value='/mock/stata/path')
        self.mock_find_stata = self.find_stata_patcher.start()
        
        # 创建StataSession实例用于测试
        self.session = StataSession()
    
    def tearDown(self):
        """每个测试方法执行后的清理"""
        self.find_stata_patcher.stop()
    
    def test_init_default(self):
        """测试默认初始化"""
        self.assertEqual(self.session.stata_path, '/mock/stata/path')
        self.assertEqual(self.session.config, {})
        self.assertFalse(self.session.session_active)
        self.assertFalse(self.session.logging_active)
        self.assertIsNone(self.session.log_path)
        
        # 验证命令模板是否正确初始化
        self.assertIn('reg', self.session.command_templates)
        self.assertIn('sum', self.session.command_templates)
        self.assertIn('import', self.session.command_templates)
        self.assertIn('export', self.session.command_templates)
        self.assertIn('tab', self.session.command_templates)
    
    def test_init_with_path(self):
        """测试指定Stata路径的初始化"""
        custom_path = '/custom/stata/path'
        session = StataSession(stata_path=custom_path)
        self.assertEqual(session.stata_path, custom_path)
        # 确认没有调用_find_stata_installation方法
        self.mock_find_stata.assert_not_called()
    
    def test_init_with_config(self):
        """测试指定配置的初始化"""
        config = {'working_dir': '/tmp', 'log_level': 'DEBUG'}
        session = StataSession(config=config)
        self.assertEqual(session.config, config)
    
    def test_configure(self):
        """测试配置更新功能"""
        config = {'working_dir': '/tmp', 'log_level': 'DEBUG'}
        self.session.configure(config)
        self.assertEqual(self.session.config, config)
        
        # 测试增量更新
        additional_config = {'timeout': 30}
        self.session.configure(additional_config)
        expected_config = {'working_dir': '/tmp', 'log_level': 'DEBUG', 'timeout': 30}
        self.assertEqual(self.session.config, expected_config)
    
    @patch('os.path.exists')
    def test_find_stata_installation(self, mock_exists):
        """测试Stata安装路径查找功能"""
        # 停止之前的patch以测试实际方法
        self.find_stata_patcher.stop()
        
        # 模拟路径存在检查
        def side_effect(path):
            return path == "/Applications/Stata/StataSE.app/Contents/MacOS/stata-se"
        
        mock_exists.side_effect = side_effect
        
        # 创建新的StataSession实例，触发_find_stata_installation
        session = StataSession()
        self.assertEqual(session.stata_path, "/Applications/Stata/StataSE.app/Contents/MacOS/stata-se")
        
        # 恢复patch
        self.find_stata_patcher.start()
    
    def test_get_command_template(self):
        """测试获取命令模板功能"""
        template = self.session.get_command_template('reg')
        self.assertEqual(template['description'], "执行线性回归分析")
        self.assertEqual(template['template'], "reg {y} {x} {options}")
        self.assertTrue(template['params']['y']['required'])
        
        # 测试获取不存在的模板
        with self.assertRaises(KeyError):
            self.session.get_command_template('nonexistent')
    
    def test_add_command_template(self):
        """测试添加命令模板功能"""
        new_template = {
            "template": "logit {y} {x} {options}",
            "description": "执行逻辑回归分析",
            "params": {
                "y": {
                    "description": "二分类因变量",
                    "required": True
                },
                "x": {
                    "description": "自变量，多个变量用空格分隔",
                    "required": True
                },
                "options": {
                    "description": "其他选项",
                    "required": False,
                    "default": ""
                }
            }
        }
        
        self.session.add_command_template('logit', new_template)
        self.assertIn('logit', self.session.command_templates)
        retrieved_template = self.session.get_command_template('logit')
        self.assertEqual(retrieved_template, new_template)
        
        # 测试添加无效模板
        invalid_template = {"template": "invalid template"}
        with self.assertRaises(ValueError):
            self.session.add_command_template('invalid', invalid_template)
    
    def test_format_command(self):
        """测试命令格式化功能"""
        command = self.session.format_command('reg', y='price', x='mpg weight', options='robust')
        self.assertEqual(command, "reg price mpg weight robust")
        
        # 测试缺少必要参数
        with self.assertRaises(ValueError):
            self.session.format_command('reg', x='mpg weight')
        
        # 测试不存在的模板
        with self.assertRaises(KeyError):
            self.session.format_command('nonexistent')
    
    def test_session_lifecycle(self):
        """测试会话生命周期管理"""
        # 测试启动会话
        self.assertFalse(self.session.session_active)
        result = self.session.start_session()
        self.assertTrue(result)
        self.assertTrue(self.session.session_active)
        
        # 测试重复启动会话
        with self.assertRaises(RuntimeError):
            self.session.start_session()
        
        # 测试结束会话
        result = self.session.end_session()
        self.assertTrue(result)
        self.assertFalse(self.session.session_active)
        
        # 测试在未启动状态下结束会话
        with self.assertRaises(RuntimeError):
            self.session.end_session()
        
        # 测试重启会话
        result = self.session.restart_session()
        self.assertTrue(result)
        self.assertTrue(self.session.session_active)
        self.session.end_session()
    
    @patch.object(StataSession, 'run_command')
    def test_run_commands(self, mock_run_command):
        """测试执行多个命令功能"""
        # 设置模拟返回值
        mock_run_command.side_effect = lambda cmd: f"执行命令: {cmd}\n结果: 命令执行成功"
        
        # 启动会话
        self.session.start_session()
        
        # 执行多个命令
        commands = ["sysuse auto, clear", "summarize", "regress price mpg weight"]
        result = self.session.run_commands(commands)
        
        # 验证每个命令都被执行
        self.assertEqual(mock_run_command.call_count, 3)
        for cmd in commands:
            mock_run_command.assert_any_call(cmd)
        
        # 验证结果包含所有命令的输出
        for cmd in commands:
            self.assertIn(cmd, result)
        
        # 测试在未启动会话的情况下执行命令
        self.session.end_session()
        with self.assertRaises(RuntimeError):
            self.session.run_commands(commands)
    
    def test_log_management(self):
        """测试日志管理功能"""
        # 启动会话
        self.session.start_session()
        
        # 测试开始记录日志
        log_path = "/tmp/stata_test.log"
        result = self.session.start_log(log_path)
        self.assertTrue(result)
        self.assertTrue(self.session.logging_active)
        self.assertEqual(self.session.log_path, log_path)
        
        # 测试重复开始记录日志
        with self.assertRaises(RuntimeError):
            self.session.start_log("/tmp/another.log")
        
        # 测试结束日志记录
        result = self.session.end_log()
        self.assertTrue(result)
        self.assertFalse(self.session.logging_active)
        self.assertIsNone(self.session.log_path)
        
        # 测试在未记录日志的情况下结束日志
        with self.assertRaises(RuntimeError):
            self.session.end_log()
        
        # 测试在未启动会话的情况下开始记录日志
        self.session.end_session()
        with self.assertRaises(RuntimeError):
            self.session.start_log(log_path)


if __name__ == '__main__':
    unittest.main()