"""
核心功能测试
"""

import pytest
from PIL import Image
import tempfile
import os
from pathlib import Path

from cool_qrcode import CoolQRCode
from cool_qrcode.exceptions import InvalidDataError, ImageGenerationError


class TestCoolQRCode:
    """CoolQRCode类的测试"""
    
    def test_init_default(self):
        """测试默认初始化"""
        qr = CoolQRCode()
        assert qr.fill_color == "black"
        assert qr.back_color == "white"
        assert not qr._data_added
    
    def test_init_custom(self):
        """测试自定义参数初始化"""
        qr = CoolQRCode(
            fill_color="blue",
            back_color="yellow",
            box_size=15,
            border=5
        )
        assert qr.fill_color == "blue"
        assert qr.back_color == "yellow"
    
    def test_add_data_success(self):
        """测试成功添加数据"""
        qr = CoolQRCode()
        qr.add_data("测试数据")
        assert qr._data_added
    
    def test_add_data_empty(self):
        """测试添加空数据"""
        qr = CoolQRCode()
        with pytest.raises(InvalidDataError):
            qr.add_data("")
    
    def test_make_image_no_data(self):
        """测试未添加数据时生成图像"""
        qr = CoolQRCode()
        with pytest.raises(ImageGenerationError):
            qr.make_image()
    
    def test_make_image_success(self):
        """测试成功生成图像"""
        qr = CoolQRCode()
        qr.add_data("测试数据")
        img = qr.make_image()
        assert img is not None  # 检查图像是否生成
        assert hasattr(img, 'save')  # 检查是否有save方法
    
    def test_save_image(self):
        """测试保存图像"""
        qr = CoolQRCode()
        qr.add_data("测试保存")
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            qr.save(tmp.name)
            assert os.path.exists(tmp.name)
            
            # 验证文件可以被PIL打开
            img = Image.open(tmp.name)
            assert isinstance(img, Image.Image)
            
            # 清理
            os.unlink(tmp.name)
    
    def test_to_bytes(self):
        """测试转换为字节数据"""
        qr = CoolQRCode()
        qr.add_data("测试字节")
        data = qr.to_bytes()
        assert isinstance(data, bytes)
        assert len(data) > 0
    
    def test_clear(self):
        """测试清除数据"""
        qr = CoolQRCode()
        qr.add_data("测试清除")
        assert qr._data_added
        
        qr.clear()
        assert not qr._data_added
    
    def test_custom_colors(self):
        """测试自定义颜色"""
        qr = CoolQRCode(fill_color="red", back_color="lightblue")
        qr.add_data("彩色二维码")
        img = qr.make_image()
        assert img is not None  # 检查图像是否生成
        assert hasattr(img, 'save')  # 检查是否有save方法


if __name__ == "__main__":
    pytest.main([__file__]) 