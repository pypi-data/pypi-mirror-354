"""
Cool QRCode - 一个用于生成个性化二维码的Python库
"""

__version__ = "0.1.0"
__author__ = "Kelvin Xu"
__email__ = "xxk59@hotmail.com"

# 导入核心类（高级用户使用）
from .core import CoolQRCode
from .exceptions import CoolQRCodeError

# 导入简化API（初学者使用）
from .simple import (
    make_cool_qrcode,        # 万能函数 - 支持所有功能组合的核心API
    make_qrcode,
    make_colorful_qrcode,
    make_qrcode_with_logo,
    make_qrcode_with_mask,
    make_pretty_qrcode,
    create_sample_logo,
    PRETTY_COLORS
)

__all__ = [
    # 核心类
    "CoolQRCode", 
    "CoolQRCodeError",
    
    # 简化API - 专为初学者设计
    "make_cool_qrcode",      # 💫 万能函数 - 支持所有效果组合的核心API
    "make_qrcode",           # 基本二维码
    "make_colorful_qrcode",  # 彩色二维码
    "make_qrcode_with_logo", # 带Logo二维码
    "make_qrcode_with_mask", # 带蒙板二维码
    "make_pretty_qrcode",    # 预设风格二维码
    "create_sample_logo",    # 创建示例Logo
    "PRETTY_COLORS"          # 预设颜色
] 