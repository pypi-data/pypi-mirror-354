import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.stata.session import StataSession


class TestFindStataInstallation(unittest.TestCase):
    """测试StataSession类的Stata安装路径查找功能"""
    
    def test_find_stata_installation_mac(self):
        """测试在Mac系统上查找Stata安装路径"""
        # 模拟os.path.exists函数，使其在检查Mac路径时返回True
        with patch('os.path.exists') as mock_exists:
            # 设置模拟函数的行为
            def side_effect(path):
                return path == "/Applications/Stata/StataSE.app/Contents/MacOS/stata-se"
            
            mock_exists.side_effect = side_effect
            
            # 创建StataSession实例，触发_find_stata_installation
            session = StataSession()
            
            # 验证找到的路径是否正确
            self.assertEqual(session.stata_path, "/Applications/Stata/StataSE.app/Contents/MacOS/stata-se")
    
    def test_find_stata_installation_not_found(self):
        """测试找不到Stata安装路径的情况"""
        # 模拟os.path.exists函数，使其总是返回False
        with patch('os.path.exists', return_value=False):
            # 验证是否抛出FileNotFoundError异常
            with self.assertRaises(FileNotFoundError):
                session = StataSession()
    
    def test_custom_stata_path(self):
        """测试指定自定义Stata路径"""
        custom_path = "/custom/stata/path"
        session = StataSession(stata_path=custom_path)
        
        # 验证是否使用了指定的路径
        self.assertEqual(session.stata_path, custom_path)


if __name__ == '__main__':
    unittest.main()