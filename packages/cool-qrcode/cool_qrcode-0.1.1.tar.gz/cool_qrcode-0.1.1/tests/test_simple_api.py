"""
简化API测试
"""

import pytest
from PIL import Image
import tempfile
import os
from pathlib import Path

from cool_qrcode import (
    make_qrcode,
    make_colorful_qrcode,
    make_qrcode_with_logo,
    make_qrcode_with_mask,
    make_pretty_qrcode,
    create_sample_logo,
    PRETTY_COLORS
)


class TestSimpleAPI:
    """简化API测试类"""
    
    def test_make_qrcode_basic(self):
        """测试基本二维码生成"""
        img = make_qrcode("测试文本")
        assert isinstance(img, Image.Image)
        assert img.size == (500, 500)  # 默认大小
    
    def test_make_qrcode_with_colors(self):
        """测试带颜色的二维码"""
        img = make_qrcode("测试文本", colors=("red", "white"))
        assert isinstance(img, Image.Image)
    
    def test_make_qrcode_circle_dots(self):
        """测试圆形码点"""
        img = make_qrcode("测试文本", dot_shape="circle")
        assert isinstance(img, Image.Image)
    
    def test_make_qrcode_custom_size(self):
        """测试自定义大小"""
        img = make_qrcode("测试文本", size=600)
        assert isinstance(img, Image.Image)
        assert img.size == (600, 600)
    
    def test_make_qrcode_save_file(self):
        """测试保存文件"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img = make_qrcode("测试保存", filename=tmp.name)
            assert os.path.exists(tmp.name)
            assert isinstance(img, Image.Image)
            # 清理
            os.unlink(tmp.name)
    
    def test_make_colorful_qrcode(self):
        """测试彩色二维码"""
        img = make_colorful_qrcode("测试彩色", "blue", "lightblue")
        assert isinstance(img, Image.Image)
    
    def test_make_colorful_qrcode_circle(self):
        """测试彩色圆形码点"""
        img = make_colorful_qrcode(
            "测试", 
            "red", 
            "pink", 
            dot_shape="circle"
        )
        assert isinstance(img, Image.Image)
    
    def test_create_sample_logo(self):
        """测试创建示例Logo"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            logo_path = create_sample_logo(tmp.name)
            assert os.path.exists(logo_path)
            assert logo_path == tmp.name
            
            # 验证是有效的图像文件
            img = Image.open(logo_path)
            assert isinstance(img, Image.Image)
            
            # 清理
            os.unlink(tmp.name)
    
    def test_make_qrcode_with_logo(self):
        """测试带Logo的二维码"""
        # 创建临时Logo
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            logo_path = create_sample_logo(tmp.name)
            
            try:
                img = make_qrcode_with_logo("测试Logo", logo_path)
                assert isinstance(img, Image.Image)
                assert img.size == (500, 500)  # 默认大小
            finally:
                # 清理
                os.unlink(logo_path)
    
    def test_make_qrcode_with_logo_options(self):
        """测试带选项的Logo二维码"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            logo_path = create_sample_logo(tmp.name)
            
            try:
                img = make_qrcode_with_logo(
                    "测试",
                    logo_path,
                    colors=("purple", "lavender"),
                    dot_shape="circle",
                    logo_circular=True
                )
                assert isinstance(img, Image.Image)
            finally:
                os.unlink(logo_path)
    
    def test_make_qrcode_with_mask(self):
        """测试带蒙板的二维码"""
        img = make_qrcode_with_mask("测试蒙板", "blue", 0.3)
        assert isinstance(img, Image.Image)
        assert img.mode == 'RGBA'  # 蒙板版本应该是RGBA模式
    
    def test_make_qrcode_with_mask_circle(self):
        """测试圆形码点蒙板"""
        img = make_qrcode_with_mask(
            "测试", 
            "red", 
            0.5, 
            dot_shape="circle"
        )
        assert isinstance(img, Image.Image)
    
    def test_make_pretty_qrcode_all_styles(self):
        """测试所有预设风格"""
        for style in PRETTY_COLORS.keys():
            img = make_pretty_qrcode("测试风格", style)
            assert isinstance(img, Image.Image)
    
    def test_make_pretty_qrcode_invalid_style(self):
        """测试无效风格"""
        # 应该回退到默认风格
        img = make_pretty_qrcode("测试", "invalid_style")
        assert isinstance(img, Image.Image)
    
    def test_pretty_colors_constant(self):
        """测试预设颜色常量"""
        assert isinstance(PRETTY_COLORS, dict)
        assert len(PRETTY_COLORS) > 0
        assert "ocean" in PRETTY_COLORS
        assert "forest" in PRETTY_COLORS
    
    def test_mask_opacity_range(self):
        """测试蒙板透明度范围"""
        # 完全透明
        img1 = make_qrcode_with_mask("测试", "blue", 0.0)
        assert isinstance(img1, Image.Image)
        
        # 完全不透明
        img2 = make_qrcode_with_mask("测试", "blue", 1.0)
        assert isinstance(img2, Image.Image)
        
        # 中等透明度
        img3 = make_qrcode_with_mask("测试", "blue", 0.5)
        assert isinstance(img3, Image.Image)
    
    def test_different_mask_colors(self):
        """测试不同的蒙板颜色"""
        colors = ["red", "green", "blue", "yellow", "purple"]
        for color in colors:
            img = make_qrcode_with_mask("测试", color, 0.3)
            assert isinstance(img, Image.Image)
    
    def test_empty_text(self):
        """测试空文本（应该报错）"""
        with pytest.raises(Exception):
            make_qrcode("")


if __name__ == "__main__":
    pytest.main([__file__]) 