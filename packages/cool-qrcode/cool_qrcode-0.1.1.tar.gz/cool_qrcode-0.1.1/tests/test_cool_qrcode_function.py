"""
万能函数 make_cool_qrcode 测试
"""

import pytest
from PIL import Image
import tempfile
import os

from cool_qrcode import make_cool_qrcode, create_sample_logo, PRETTY_COLORS
from cool_qrcode.simple import _color_to_rgb


class TestMakeCoolQRCode:
    """万能函数测试类"""
    
    def test_basic_usage(self):
        """测试基础使用"""
        img = make_cool_qrcode("测试文本")
        assert isinstance(img, Image.Image)
        assert img.size == (500, 500)  # 默认大小
    
    def test_custom_colors(self):
        """测试自定义颜色"""
        img = make_cool_qrcode("测试", colors=("red", "white"))
        assert isinstance(img, Image.Image)
    
    def test_common_colors_support(self):
        """测试常用颜色支持"""
        common_colors = [
            "aqua", "black", "blue", "fuchsia", "grey", "lime", 
            "maroon", "navy", "olive", "purple", "red", "silver", 
            "teal", "white", "yellow", "orange"
        ]
        
        # 测试颜色转换函数
        for color in common_colors:
            rgb = _color_to_rgb(color)
            assert isinstance(rgb, tuple)
            assert len(rgb) == 3
            assert all(0 <= value <= 255 for value in rgb)
        
        # 测试在二维码生成中使用
        for color in common_colors:
            img = make_cool_qrcode(
                f"测试{color}颜色",
                colors=(color, "white")
            )
            assert isinstance(img, Image.Image)
    
    def test_preset_styles(self):
        """测试预设风格"""
        for style in PRETTY_COLORS.keys():
            img = make_cool_qrcode("测试", style=style)
            assert isinstance(img, Image.Image)
    
    def test_invalid_style(self):
        """测试无效风格"""
        img = make_cool_qrcode("测试", style="invalid_style")
        assert isinstance(img, Image.Image)  # 应该回退到默认风格
    
    def test_circle_dots(self):
        """测试圆形码点"""
        img = make_cool_qrcode("测试", dot_shape="circle")
        assert isinstance(img, Image.Image)
    
    def test_custom_size(self):
        """测试自定义尺寸"""
        img = make_cool_qrcode("测试", size=600)
        assert isinstance(img, Image.Image)
        assert img.size == (600, 600)
    
    def test_with_logo(self):
        """测试带Logo"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            logo_path = create_sample_logo(tmp.name)
            
            try:
                img = make_cool_qrcode("测试", logo_path=logo_path)
                assert isinstance(img, Image.Image)
            finally:
                os.unlink(logo_path)
    
    def test_with_mask(self):
        """测试带蒙板"""
        img = make_cool_qrcode("测试", mask_color="blue", mask_opacity=0.3)
        assert isinstance(img, Image.Image)
        assert img.mode == 'RGBA'  # 蒙板版本应该是RGBA模式
    
    def test_logo_circular_option(self):
        """测试Logo圆形选项"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            logo_path = create_sample_logo(tmp.name)
            
            try:
                # 圆形Logo
                img1 = make_cool_qrcode("测试", logo_path=logo_path, logo_circular=True)
                assert isinstance(img1, Image.Image)
                
                # 方形Logo
                img2 = make_cool_qrcode("测试", logo_path=logo_path, logo_circular=False)
                assert isinstance(img2, Image.Image)
            finally:
                os.unlink(logo_path)
    
    def test_mask_opacity_range(self):
        """测试蒙板透明度范围"""
        opacities = [0.0, 0.5, 1.0]
        for opacity in opacities:
            img = make_cool_qrcode("测试", mask_color="red", mask_opacity=opacity)
            assert isinstance(img, Image.Image)
    
    def test_color_style_priority(self):
        """测试颜色和风格的优先级"""
        # style 应该优先于 colors
        img = make_cool_qrcode("测试", colors=("red", "white"), style="ocean")
        assert isinstance(img, Image.Image)
        # 实际颜色应该是ocean风格的颜色，而不是red/white
    
    def test_combination_effects(self):
        """测试组合效果"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            logo_path = create_sample_logo(tmp.name)
            
            try:
                # 所有效果组合
                img = make_cool_qrcode(
                    "测试组合",
                    style="berry",
                    dot_shape="circle",
                    logo_path=logo_path,
                    logo_circular=True,
                    mask_color="purple",
                    mask_opacity=0.2,
                    size=500
                )
                assert isinstance(img, Image.Image)
                assert img.size == (500, 500)
            finally:
                os.unlink(logo_path)
    
    def test_save_file(self):
        """测试保存文件"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img = make_cool_qrcode("测试保存", filename=tmp.name)
            assert os.path.exists(tmp.name)
            assert isinstance(img, Image.Image)
            # 清理
            os.unlink(tmp.name)
    
    def test_mask_without_other_effects(self):
        """测试单独使用蒙板"""
        img = make_cool_qrcode(
            "仅蒙板",
            mask_color="green",
            mask_opacity=0.4
        )
        assert isinstance(img, Image.Image)
        assert img.mode == 'RGBA'
    
    def test_logo_without_other_effects(self):
        """测试单独使用Logo"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            logo_path = create_sample_logo(tmp.name)
            
            try:
                img = make_cool_qrcode("仅Logo", logo_path=logo_path)
                assert isinstance(img, Image.Image)
            finally:
                os.unlink(logo_path)
    
    def test_different_mask_colors(self):
        """测试不同蒙板颜色"""
        colors = ["red", "green", "blue", "yellow", "purple"]
        for color in colors:
            img = make_cool_qrcode("测试", mask_color=color, mask_opacity=0.3)
            assert isinstance(img, Image.Image)
    
    def test_large_size_with_effects(self):
        """测试大尺寸与效果组合"""
        img = make_cool_qrcode(
            "大尺寸测试",
            style="forest",
            dot_shape="circle",
            size=800
        )
        assert isinstance(img, Image.Image)
        assert img.size == (800, 800)
    
    def test_small_size_with_effects(self):
        """测试小尺寸与效果组合"""
        img = make_cool_qrcode(
            "小尺寸测试",
            colors=("blue", "lightblue"),
            dot_shape="circle",
            size=200
        )
        assert isinstance(img, Image.Image)
        assert img.size == (200, 200)
    
    def test_empty_text_error(self):
        """测试空文本（应该报错）"""
        with pytest.raises(Exception):
            make_cool_qrcode("")
    
    def test_nonexistent_logo_error(self):
        """测试不存在的Logo文件（应该报错）"""
        with pytest.raises(Exception):
            make_cool_qrcode("测试", logo_path="nonexistent_logo.png")


if __name__ == "__main__":
    pytest.main([__file__]) 