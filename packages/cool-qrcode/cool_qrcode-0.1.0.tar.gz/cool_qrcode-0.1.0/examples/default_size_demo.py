#!/usr/bin/env python3
"""
Cool QRCode 默认大小演示
展示默认大小为500像素的二维码
"""

from cool_qrcode import make_cool_qrcode
from PIL import Image
import os

def show_image_info(img, filename):
    """显示图像信息"""
    print(f"图像 '{filename}':")
    print(f"  - 尺寸: {img.size[0]} x {img.size[1]} 像素")
    print(f"  - 模式: {img.mode}")
    
    # 保存图像
    img.save(filename)
    print(f"  - 已保存: {filename}")
    
    # 获取文件大小
    file_size = os.path.getsize(filename) / 1024  # KB
    print(f"  - 文件大小: {file_size:.2f} KB")
    print()


def main():
    """主函数"""
    print("🖼️ Cool QRCode 默认大小演示")
    print("=" * 40)
    print("默认大小为 500 x 500 像素")
    print()
    
    # 示例1: 默认大小 (500像素)
    qr1 = make_cool_qrcode(
        "这是默认大小 (500x500) 的二维码",
        style="ocean"
    )
    show_image_info(qr1, "默认大小.png")
    
    # 示例2: 自定义大小对比
    sizes = [300, 500, 800]
    for size in sizes:
        qr = make_cool_qrcode(
            f"{size}x{size} 像素的二维码",
            size=size,
            style="berry",
            dot_shape="circle"
        )
        show_image_info(qr, f"{size}像素.png")


if __name__ == "__main__":
    main() 