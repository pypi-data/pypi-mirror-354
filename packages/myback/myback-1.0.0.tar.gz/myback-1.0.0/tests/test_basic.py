"""
基础测试 - 测试包的基本功能
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_import_myback():
    """测试能否正确导入myback包"""
    try:
        import myback
        assert hasattr(myback, '__version__')
        assert hasattr(myback, 'main')
        print(f"成功导入myback，版本: {myback.__version__}")
    except ImportError as e:
        pytest.fail(f"无法导入myback包: {e}")


def test_import_modules():
    """测试能否导入各个模块"""
    try:
        from myback import dialog, tools
        from myback.main import main
        assert dialog.FeedbackDialog is not None
        assert tools.collect_feedback is not None
        assert callable(main)
        print("成功导入所有模块")
    except ImportError as e:
        pytest.fail(f"无法导入模块: {e}")


def test_version_format():
    """测试版本号格式"""
    import myback
    version = myback.__version__
    
    # 检查版本号格式（应该是x.y.z格式）
    parts = version.split('.')
    assert len(parts) >= 2, f"版本号格式不正确: {version}"
    
    for part in parts:
        assert part.isdigit(), f"版本号部分应该是数字: {part}"
    
    print(f"版本号格式正确: {version}")


def test_dialog_class():
    """测试FeedbackDialog类"""
    from myback.dialog import FeedbackDialog
    
    # 测试创建实例
    dialog = FeedbackDialog("测试工作汇报", 60)
    assert dialog.work_summary == "测试工作汇报"
    assert dialog.timeout_seconds == 60
    assert dialog.selected_images == []
    
    print("FeedbackDialog类测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
