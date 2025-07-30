"""
高级特性测试
"""

import pytest
from PIL import Image, ImageDraw
import tempfile
import os
from pathlib import Path

from cool_qrcode import CoolQRCode
from cool_qrcode.exceptions import InvalidDataError, ImageGenerationError, InvalidLogoError


class TestAdvancedFeatures:
    """高级特性测试类"""
    
    @pytest.fixture
    def sample_logo(self):
        """创建测试用的Logo文件"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            # 创建一个简单的测试Logo
            logo = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
            draw = ImageDraw.Draw(logo)
            draw.ellipse((20, 20, 80, 80), fill='blue')
            logo.save(tmp.name)
            yield tmp.name
            # 清理
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
    
    def test_make_custom_image_square(self):
        """测试生成方形码点的自定义图像"""
        qr = CoolQRCode()
        qr.add_data("测试方形码点")
        
        img = qr.make_custom_image(size=400, dot_shape="square")
        assert isinstance(img, Image.Image)
        assert img.size == (400, 400)
    
    def test_make_custom_image_circle(self):
        """测试生成圆形码点的自定义图像"""
        qr = CoolQRCode()
        qr.add_data("测试圆形码点")
        
        img = qr.make_custom_image(size=500, dot_shape="circle")
        assert isinstance(img, Image.Image)
        assert img.size == (500, 500)
    
    def test_make_custom_image_no_data(self):
        """测试未添加数据时生成自定义图像"""
        qr = CoolQRCode()
        with pytest.raises(ImageGenerationError):
            qr.make_custom_image()
    
    def test_add_logo_circular(self, sample_logo):
        """测试添加圆形Logo"""
        qr = CoolQRCode()
        qr.add_data("测试圆形Logo")
        
        img = qr.add_logo(sample_logo, circular=True)
        assert img is not None  # 检查图像是否生成
        assert hasattr(img, 'save')  # 检查是否有save方法
    
    def test_add_logo_square(self, sample_logo):
        """测试添加方形Logo"""
        qr = CoolQRCode()
        qr.add_data("测试方形Logo")
        
        img = qr.add_logo(sample_logo, circular=False)
        assert img is not None  # 检查图像是否生成
        assert hasattr(img, 'save')  # 检查是否有save方法
    
    def test_add_logo_to_custom(self, sample_logo):
        """测试在自定义样式二维码中添加Logo"""
        qr = CoolQRCode()
        qr.add_data("测试自定义样式Logo")
        
        img = qr.add_logo_to_custom(
            logo_path=sample_logo,
            size=600,
            dot_shape="circle",
            circular_logo=True
        )
        assert isinstance(img, Image.Image)
        assert img.size == (600, 600)
    
    def test_add_logo_to_custom_square_dots(self, sample_logo):
        """测试在方形码点二维码中添加Logo"""
        qr = CoolQRCode()
        qr.add_data("测试方形码点Logo")
        
        img = qr.add_logo_to_custom(
            logo_path=sample_logo,
            size=400,
            dot_shape="square",
            circular_logo=False
        )
        assert isinstance(img, Image.Image)
        assert img.size == (400, 400)
    
    def test_add_logo_to_custom_nonexistent_logo(self):
        """测试使用不存在的Logo文件"""
        qr = CoolQRCode()
        qr.add_data("测试不存在Logo")
        
        with pytest.raises(InvalidLogoError):
            qr.add_logo_to_custom("nonexistent_logo.png")
    
    def test_custom_colors_with_custom_image(self):
        """测试自定义颜色的自定义图像"""
        qr = CoolQRCode(
            fill_color="#FF6B6B",
            back_color="#F8F9FA"
        )
        qr.add_data("测试自定义颜色")
        
        img = qr.make_custom_image(size=300, dot_shape="circle")
        assert isinstance(img, Image.Image)
        assert img.size == (300, 300)
    
    def test_large_size_custom_image(self):
        """测试大尺寸自定义图像"""
        qr = CoolQRCode()
        qr.add_data("测试大尺寸")
        
        img = qr.make_custom_image(size=1000, dot_shape="square")
        assert isinstance(img, Image.Image)
        assert img.size == (1000, 1000)
    
    def test_small_size_custom_image(self):
        """测试小尺寸自定义图像"""
        qr = CoolQRCode()
        qr.add_data("测试小尺寸")
        
        img = qr.make_custom_image(size=200, dot_shape="circle")
        assert isinstance(img, Image.Image)
        assert img.size == (200, 200)
    
    def test_circular_border_logo(self, sample_logo):
        """测试带圆形边框的Logo"""
        qr = CoolQRCode()
        qr.add_data("测试圆形边框Logo")
        
        img = qr.add_logo(
            sample_logo,
            circular=True,
            border_size=5,
            size_ratio=0.3
        )
        assert img is not None  # 检查图像是否生成
        assert hasattr(img, 'save')  # 检查是否有save方法
    
    def test_invalid_dot_shape(self):
        """测试无效的码点形状参数"""
        qr = CoolQRCode()
        qr.add_data("测试数据")
        
        # 虽然类型提示限制了参数，但我们还是测试运行时行为
        # 无效的dot_shape会被当作'square'处理
        img = qr.make_custom_image(size=300, dot_shape="invalid")
        assert isinstance(img, Image.Image)


if __name__ == "__main__":
    pytest.main([__file__]) 