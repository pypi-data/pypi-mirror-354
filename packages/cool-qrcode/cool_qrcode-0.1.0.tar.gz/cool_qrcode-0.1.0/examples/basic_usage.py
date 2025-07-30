#!/usr/bin/env python3
"""
Cool QRCode 基础使用示例
"""

from cool_qrcode import CoolQRCode
from qrcode.constants import ERROR_CORRECT_H


def basic_example():
    """基础二维码生成示例"""
    print("生成基础二维码...")
    
    qr = CoolQRCode()
    qr.add_data("https://github.com/xxk59/cool-qrcode")
    img = qr.make_image()
    img.save("basic_qrcode.png")
    print("✅ 基础二维码已保存为 basic_qrcode.png")


def colorful_example():
    """彩色二维码示例"""
    print("生成彩色二维码...")
    
    qr = CoolQRCode(
        fill_color="darkblue",
        back_color="lightblue",
        box_size=12,
        border=6
    )
    qr.add_data("Cool QRCode - 个性化二维码生成器")
    img = qr.make_image()
    img.save("colorful_qrcode.png")
    print("✅ 彩色二维码已保存为 colorful_qrcode.png")


def high_quality_example():
    """高质量二维码示例"""
    print("生成高质量二维码...")
    
    qr = CoolQRCode(
        version=5,  # 更大的版本支持更多数据
        error_correction=ERROR_CORRECT_H,  # 最高纠错级别
        box_size=15,  # 更大的像素块
        border=4,
        fill_color="black",
        back_color="white"
    )
    
    # 添加更多数据
    data = """
    Cool QRCode 是一个强大的Python库，用于生成个性化二维码。
    特性包括：
    - 自定义颜色
    - 添加Logo
    - 多种纠错级别
    - 简洁的API
    访问项目：https://github.com/xxk59/cool-qrcode
    """
    
    qr.add_data(data.strip())
    img = qr.make_image()
    img.save("high_quality_qrcode.png")
    print("✅ 高质量二维码已保存为 high_quality_qrcode.png")


def bytes_example():
    """字节数据示例"""
    print("生成字节数据...")
    
    qr = CoolQRCode(fill_color="green", back_color="white")
    qr.add_data("转换为字节数据的二维码")
    
    # 获取PNG格式的字节数据
    png_data = qr.to_bytes("PNG")
    print(f"✅ PNG数据大小: {len(png_data)} 字节")
    
    # 获取JPEG格式的字节数据
    jpeg_data = qr.to_bytes("JPEG")
    print(f"✅ JPEG数据大小: {len(jpeg_data)} 字节")


def main():
    """主函数"""
    print("🔥 Cool QRCode 示例演示")
    print("=" * 40)
    
    try:
        basic_example()
        print()
        
        colorful_example()
        print()
        
        high_quality_example()
        print()
        
        bytes_example()
        print()
        
        print("🎉 所有示例运行完成！")
        print("请查看生成的二维码图片文件。")
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")


if __name__ == "__main__":
    main() 