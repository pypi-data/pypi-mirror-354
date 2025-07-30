"""
Cool QRCode 简化API - 专为初学者设计
"""

from typing import Union, Optional, Literal
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
import tempfile
import os

from .core import CoolQRCode
from .exceptions import CoolQRCodeError


def make_cool_qrcode(
    data: str,
    filename: Optional[str] = None,
    size: int = 500,
    # 颜色选项
    fill_color: str = "black",
    back_color: str = "white",
    style: Optional[str] = None,
    # 形状选项
    dot_shape: Literal["square", "circle"] = "square",
    # Logo选项
    logo_path: Optional[str] = None,
    logo_circular: bool = True,
    # 蒙板选项
    mask_color: Optional[str] = None,
    mask_opacity: float = 0.3
) -> Image.Image:
    """
    生成自定义二维码 - 万能函数，支持多种效果组合

    这是Cool QRCode库的核心函数，支持所有功能特性的组合使用。可以生成带有自定义颜色、
    形状、Logo和蒙板效果的二维码，所有效果可以任意组合。

    参数:
        data (str): 
            二维码内容，必须非空。可以是网址、文本、联系信息等。
        
        filename (str, 可选): 
            保存文件名。如果提供，二维码会保存到该文件。默认为None，不保存文件。
        
        size (int, 可选): 
            图片大小（像素）。默认为500像素。
        
        fill_color (str, 可选):
            前景色（码点颜色），默认为"black"。
            可使用颜色名称或十六进制颜色代码("#FF5733")。
            当同时指定颜色和style时，style优先。
            
        back_color (str, 可选):
            背景色，默认为"white"。
            可使用颜色名称或十六进制颜色代码("#F8F9FA")。
            当同时指定颜色和style时，style优先。
        
        style (str, 可选): 
            预设风格，可选值: "ocean", "forest", "sunset", "berry", 
            "fire", "mint", "chocolate", "night"。
            当同时指定颜色和style时，style优先。
        
        dot_shape (str, 可选): 
            码点形状。可选值: "square"(方形) 或 "circle"(圆形)。默认为"square"。
        
        logo_path (str, 可选): 
            Logo图片路径。如果提供，会在二维码中央添加Logo。默认为None。
        
        logo_circular (bool, 可选): 
            Logo是否为圆形。如果为True，Logo会被裁剪成圆形。默认为True。
        
        mask_color (str, 可选): 
            蒙板颜色。如果提供，会添加半透明蒙板效果。默认为None。
        
        mask_opacity (float, 可选): 
            蒙板透明度，范围0.0-1.0。0.0为完全透明，1.0为完全不透明。默认为0.3。

    返回:
        PIL.Image.Image: 生成的二维码图像对象

    示例:
        # 基本用法
        make_cool_qrcode("Hello, World!")
        
        # 保存到文件
        make_cool_qrcode("Hello, World!", filename="my_qr.png")
        
        # 自定义颜色
        make_cool_qrcode("Hello", fill_color="blue", back_color="white")
        
        # 使用预设风格
        make_cool_qrcode("Hello", style="ocean")
        
        # 圆形码点
        make_cool_qrcode("Hello", dot_shape="circle")
        
        # 添加Logo
        make_cool_qrcode("Hello", logo_path="logo.png")
        
        # 添加蒙板效果
        make_cool_qrcode("Hello", mask_color="blue", mask_opacity=0.3)
        
        # 组合多种效果
        make_cool_qrcode(
            "综合效果示例",
            style="berry",
            dot_shape="circle",
            logo_path="logo.png",
            mask_color="purple",
            mask_opacity=0.2,
            size=600,
            filename="cool_qr.png"
        )
    
    注意:
        1. 组合效果时，style会覆盖fill_color和back_color设置
        2. 当使用蒙板效果时，图像会自动转换为RGBA模式
        3. 当logo_path不存在时，会抛出异常
        4. 如果指定filename，函数会自动保存图像并打印确认信息
    """
    
    # 1. 确定颜色
    if style:
        # 使用预设风格
        if style not in PRETTY_COLORS:
            print(f"⚠️ 风格 '{style}' 不存在，使用默认风格 'ocean'")
            style = "ocean"
        fill_color, back_color = PRETTY_COLORS[style]
    
    # 2. 创建基础二维码
    qr = CoolQRCode(fill_color=fill_color, back_color=back_color)
    qr.add_data(data)
    
    # 3. 生成图像（根据是否有Logo选择不同方法）
    if logo_path:
        # 有Logo的情况
        img = qr.add_logo_to_custom(
            logo_path=logo_path,
            size=size,
            dot_shape=dot_shape,
            logo_size_ratio=0.2,
            circular_logo=logo_circular
        )
    else:
        # 无Logo的情况
        img = qr.make_custom_image(size=size, dot_shape=dot_shape)
    
    # 4. 应用蒙板效果（如果指定）
    if mask_color:
        # 创建半透明蒙板
        mask = Image.new('RGBA', (size, size), (*_color_to_rgb(mask_color), int(255 * mask_opacity)))
        
        # 将原图转换为RGBA模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 应用蒙板
        img = Image.alpha_composite(img, mask)
    
    # 5. 保存文件（如果指定）
    if filename:
        img.save(filename)
        print(f"✅ 酷炫二维码已保存为 {filename}")
    
    return img


def make_qrcode(
    data: str,
    filename: Optional[str] = None,
    size: int = 500,
    fill_color: str = "black",
    back_color: str = "white",
    dot_shape: Literal["square", "circle"] = "square"
) -> Image.Image:
    """
    生成基本二维码 - 最简单的方式
    
    参数:
        data: 二维码内容
        filename: 保存文件名（可选）
        size: 图片大小（像素）
        fill_color: 前景色（码点颜色）
        back_color: 背景色
        dot_shape: 码点形状 "square"(方形) 或 "circle"(圆形)
    
    返回:
        生成的二维码图片
    
    示例:
        # 最简单的用法
        make_qrcode("Hello World!")
        
        # 保存到文件
        make_qrcode("Hello World!", filename="my_qr.png")
        
        # 彩色二维码
        make_qrcode("Hello World!", fill_color="red", back_color="yellow")
        
        # 圆形码点
        make_qrcode("Hello World!", dot_shape="circle")
    """
    return make_cool_qrcode(
        data=data,
        filename=filename,
        size=size,
        fill_color=fill_color,
        back_color=back_color,
        dot_shape=dot_shape
    )


def make_colorful_qrcode(
    data: str,
    fill_color: str = "blue",
    back_color: str = "lightblue",
    filename: Optional[str] = None,
    size: int = 500,
    dot_shape: Literal["square", "circle"] = "square"
) -> Image.Image:
    """
    生成彩色二维码
    
    参数:
        data: 二维码内容
        fill_color: 前景色（码点颜色）
        back_color: 背景色
        filename: 保存文件名（可选）
        size: 图片大小
        dot_shape: 码点形状
    
    示例:
        # 蓝色二维码
        make_colorful_qrcode("Hello!", "blue", "lightblue")
        
        # 红色圆点二维码
        make_colorful_qrcode("Hello!", "red", "pink", dot_shape="circle")
    """
    return make_cool_qrcode(
        data=data,
        filename=filename,
        size=size,
        fill_color=fill_color,
        back_color=back_color,
        dot_shape=dot_shape
    )


def make_qrcode_with_logo(
    data: str,
    logo_path: str,
    filename: Optional[str] = None,
    size: int = 500,
    fill_color: str = "black",
    back_color: str = "white",
    dot_shape: Literal["square", "circle"] = "square",
    logo_circular: bool = True
) -> Image.Image:
    """
    生成带Logo的二维码
    
    参数:
        data: 二维码内容
        logo_path: Logo图片文件路径
        filename: 保存文件名（可选）
        size: 图片大小
        fill_color: 前景色（码点颜色）
        back_color: 背景色
        dot_shape: 码点形状
        logo_circular: Logo是否为圆形
    
    示例:
        # 带Logo的二维码
        make_qrcode_with_logo("Hello!", "my_logo.png")
        
        # 彩色+圆点+圆形Logo
        make_qrcode_with_logo(
            "Hello!", 
            "logo.png", 
            fill_color="purple",
            back_color="lavender",
            dot_shape="circle"
        )
    """
    return make_cool_qrcode(
        data=data,
        filename=filename,
        size=size,
        fill_color=fill_color,
        back_color=back_color,
        dot_shape=dot_shape,
        logo_path=logo_path,
        logo_circular=logo_circular
    )


def make_qrcode_with_mask(
    data: str,
    mask_color: str = "blue",
    mask_opacity: float = 0.3,
    filename: Optional[str] = None,
    size: int = 500,
    fill_color: str = "black",
    back_color: str = "white",
    dot_shape: Literal["square", "circle"] = "square"
) -> Image.Image:
    """
    生成带半透明蒙板的二维码
    
    参数:
        data: 二维码内容
        mask_color: 蒙板颜色
        mask_opacity: 蒙板透明度 (0.0-1.0, 0完全透明，1完全不透明)
        filename: 保存文件名（可选）
        size: 图片大小
        fill_color: 前景色（码点颜色）
        back_color: 背景色
        dot_shape: 码点形状
    
    示例:
        # 蓝色半透明蒙板
        make_qrcode_with_mask("Hello!", "blue", 0.3)
        
        # 红色蒙板圆点二维码
        make_qrcode_with_mask(
            "Hello!", 
            mask_color="red", 
            mask_opacity=0.4,
            dot_shape="circle"
        )
    """
    return make_cool_qrcode(
        data=data,
        filename=filename,
        size=size,
        fill_color=fill_color,
        back_color=back_color,
        dot_shape=dot_shape,
        mask_color=mask_color,
        mask_opacity=mask_opacity
    )


def create_sample_logo(filename: str = "sample_logo.png") -> str:
    """
    创建一个示例Logo文件供练习使用
    
    参数:
        filename: Logo文件名
    
    返回:
        创建的Logo文件路径
    
    示例:
        # 创建示例Logo
        logo_path = create_sample_logo()
        make_qrcode_with_logo("Hello!", logo_path)
    """
    from PIL import ImageFont
    
    # 创建Logo
    logo_size = 120
    logo = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    
    # 绘制彩色圆形背景
    draw.ellipse((10, 10, logo_size-10, logo_size-10), fill='#FF6B6B')
    
    # 添加文字
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
    except:
        # 使用默认字体
        font = ImageFont.load_default()
    
    # 绘制白色文字 "QR"
    text = "QR"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (logo_size - text_width) // 2
    text_y = (logo_size - text_height) // 2
    
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    # 保存Logo
    logo.save(filename)
    print(f"✅ 示例Logo已创建: {filename}")
    
    return filename


def _color_to_rgb(color: str) -> tuple:
    """将颜色名称转换为RGB值"""
    color_map = {
        # 基础颜色
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (128, 0, 128),
        'orange': (255, 165, 0),
        'pink': (255, 192, 203),
        'cyan': (0, 255, 255),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
        
        # 添加更多常用颜色
        'aqua': (0, 255, 255),      # 水绿色
        'fuchsia': (255, 0, 255),   # 紫红色
        'lime': (0, 255, 0),        # 酸橙色
        'maroon': (128, 0, 0),      # 栗色
        'navy': (0, 0, 128),        # 海军蓝
        'olive': (128, 128, 0),     # 橄榄色
        'silver': (192, 192, 192),  # 银色
        'teal': (0, 128, 128),      # 蓝绿色
        
        # 扩展颜色
        'lightblue': (173, 216, 230),
        'lightgreen': (144, 238, 144),
        'lightcyan': (224, 255, 255),
        'lightyellow': (255, 255, 224),
        'lavender': (230, 230, 250),
        'lightgray': (211, 211, 211),
        'lightpink': (255, 182, 193),
        'darkblue': (0, 0, 139),
        'darkgreen': (0, 100, 0),
        'darkorange': (255, 140, 0),
        'darkred': (139, 0, 0),
        'brown': (165, 42, 42),
        'wheat': (245, 222, 179),
    }
    
    color_lower = color.lower()
    if color_lower in color_map:
        return color_map[color_lower]
    
    # 如果是十六进制颜色
    if color.startswith('#'):
        try:
            hex_color = color[1:]
            if len(hex_color) == 6:
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            pass
    
    # 默认返回黑色
    return (0, 0, 0)


# 预设的漂亮颜色组合
PRETTY_COLORS = {
    "ocean": ("darkblue", "lightblue"),
    "forest": ("darkgreen", "lightgreen"), 
    "sunset": ("darkorange", "lightyellow"),
    "berry": ("purple", "lavender"),
    "fire": ("red", "pink"),
    "mint": ("teal", "lightcyan"),
    "chocolate": ("brown", "wheat"),
    "night": ("navy", "lightgray")
}


def make_pretty_qrcode(
    data: str,
    style: str = "ocean",
    filename: Optional[str] = None,
    size: int = 500,
    dot_shape: Literal["square", "circle"] = "circle"
) -> Image.Image:
    """
    使用预设的漂亮颜色生成二维码
    
    参数:
        data: 二维码内容
        style: 颜色风格，可选: "ocean", "forest", "sunset", "berry", 
               "fire", "mint", "chocolate", "night"
        filename: 保存文件名（可选）
        size: 图片大小
        dot_shape: 码点形状
    
    示例:
        # 海洋风格
        make_pretty_qrcode("Hello!", "ocean")
        
        # 浆果风格圆点
        make_pretty_qrcode("Hello!", "berry", dot_shape="circle")
    """
    if style not in PRETTY_COLORS:
        print(f"⚠️ 风格 '{style}' 不存在，使用默认风格 'ocean'")
        style = "ocean"
    
    return make_cool_qrcode(
        data=data,
        filename=filename,
        size=size,
        style=style,
        dot_shape=dot_shape
    ) 