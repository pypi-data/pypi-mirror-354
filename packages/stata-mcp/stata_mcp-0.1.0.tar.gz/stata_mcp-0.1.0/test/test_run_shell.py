import unittest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.run_shell import (
    run_single_command,
    run_multiple_commands,
    run_command_with_logging,
    run_command_async,
    run_command_with_timeout,
    run_command_as_user,
    run_command_in_directory,
    run_command_with_env
)


class TestRunShell(unittest.TestCase):
    """测试run_shell模块的功能"""
    
    def test_run_single_command(self):
        """测试运行单个命令的功能"""
        with patch('subprocess.run') as mock_run:
            # 设置模拟返回值
            mock_process = MagicMock()
            mock_process.stdout = "Command executed successfully"
            mock_process.returncode = 0
            mock_run.return_value = mock_process
            
            # 调用被测试的函数
            result = run_single_command("echo 'Hello World'")
            
            # 验证subprocess.run被正确调用
            mock_run.assert_called_once()
            # 验证返回结果
            self.assertEqual(result, "命令执行成功")
    
    def test_run_multiple_commands(self):
        """测试运行多个命令的功能"""
        with patch('src.utils.run_shell.run_single_command') as mock_run_single:
            # 设置模拟返回值
            mock_run_single.side_effect = ["Result1", "Result2", "Result3"]
            
            # 调用被测试的函数
            commands = ["cmd1", "cmd2", "cmd3"]
            result = run_multiple_commands(commands)
            
            # 验证run_single_command被正确调用
            self.assertEqual(mock_run_single.call_count, 3)
            for i, cmd in enumerate(commands):
                mock_run_single.assert_any_call(cmd)
            
            # 验证返回结果
            self.assertIn("Result1", result)
            self.assertIn("Result2", result)
            self.assertIn("Result3", result)
    
    def test_run_command_with_logging(self):
        """测试带日志的命令执行功能"""
        with patch('subprocess.Popen') as mock_popen:
            # 设置模拟返回值
            mock_process = MagicMock()
            mock_process.communicate.return_value = (b"stdout", b"stderr")
            mock_process.returncode = 0
            mock_popen.return_value = mock_process
            
            # 调用被测试的函数
            stdout, stderr = run_command_with_logging("echo 'Hello World'")
            
            # 验证subprocess.Popen被正确调用
            mock_popen.assert_called_once()
            # 验证返回结果
            self.assertEqual(stdout, "stdout")
            self.assertEqual(stderr, "stderr")
    
    @patch('asyncio.create_subprocess_shell')
    @patch('asyncio.run')
    def test_run_command_async(self, mock_run, mock_create_subprocess):
        """测试异步命令执行功能"""
        # 设置模拟返回值
        mock_process = MagicMock()
        mock_process.communicate = MagicMock(return_value=(b"async output", b""))
        mock_process.returncode = 0
        mock_create_subprocess.return_value = mock_process
        mock_run.return_value = "async output"
        
        # 调用被测试的函数
        result = run_command_async("echo 'Hello World'")
        
        # 验证asyncio.run被正确调用
        mock_run.assert_called_once()
        # 验证返回结果
        self.assertEqual(result, "async output")
    
    def test_run_command_with_timeout(self):
        """测试带超时的命令执行功能"""
        with patch('subprocess.run') as mock_run:
            # 设置模拟返回值
            mock_process = MagicMock()
            mock_process.stdout = "Command executed successfully"
            mock_process.returncode = 0
            mock_run.return_value = mock_process
            
            # 调用被测试的函数
            result = run_command_with_timeout("echo 'Hello World'", timeout=10)
            
            # 验证subprocess.run被正确调用，并且传入了timeout参数
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            self.assertEqual(kwargs.get('timeout'), 10)
            
            # 验证返回结果
            self.assertEqual(result, "命令执行成功")
            
            # 测试超时异常
            # 重置mock对象的side_effect
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=10)
            # 验证是否正确抛出TimeoutError异常
            with self.assertRaises(TimeoutError):
                run_command_with_timeout("sleep 20", timeout=10)
    
    def test_run_command_as_user(self):
        """测试以特定用户身份执行命令的功能"""
        with patch('subprocess.run') as mock_run:
            # 设置模拟返回值
            mock_process = MagicMock()
            mock_process.stdout = "Command executed successfully"
            mock_process.returncode = 0
            mock_run.return_value = mock_process
            
            # 调用被测试的函数
            result = run_command_as_user("echo 'Hello World'", username="testuser")
            
            # 验证subprocess.run被正确调用，并且命令被修改为使用sudo -u
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            self.assertIn("sudo -u testuser", kwargs.get('args', [''])[0])
            
            # 验证返回结果
            self.assertEqual(result, "命令执行成功")
    
    def test_run_command_in_directory(self):
        """测试在特定目录中执行命令的功能"""
        with patch('subprocess.run') as mock_run:
            # 设置模拟返回值
            mock_process = MagicMock()
            mock_process.stdout = "Command executed successfully"
            mock_process.returncode = 0
            mock_run.return_value = mock_process
            
            # 调用被测试的函数
            result = run_command_in_directory("echo 'Hello World'", directory="/tmp")
            
            # 验证subprocess.run被正确调用，并且cwd参数被设置
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            self.assertEqual(kwargs.get('cwd'), "/tmp")
            
            # 验证返回结果
            self.assertEqual(result, "命令执行成功")
    
    def test_run_command_with_env(self):
        """测试使用特定环境变量执行命令的功能"""
        with patch('subprocess.run') as mock_run:
            # 设置模拟返回值
            mock_process = MagicMock()
            mock_process.stdout = "Command executed successfully"
            mock_process.returncode = 0
            mock_run.return_value = mock_process
            
            # 调用被测试的函数
            env_vars = {"TEST_VAR": "test_value"}
            result = run_command_with_env("echo $TEST_VAR", env_vars=env_vars)
            
            # 验证subprocess.run被正确调用，并且env参数包含指定的环境变量
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            self.assertIn("TEST_VAR", kwargs.get('env', {}))
            self.assertEqual(kwargs.get('env', {}).get("TEST_VAR"), "test_value")
            
            # 验证返回结果
            self.assertEqual(result, "命令执行成功")


if __name__ == '__main__':
    unittest.main()