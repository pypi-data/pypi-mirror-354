#!/usr/bin/env python3
"""
Cool QRCode 高级特性使用示例
展示圆形码点、圆形Logo等新功能
"""

from cool_qrcode import CoolQRCode
from qrcode.constants import ERROR_CORRECT_H
import os


def create_sample_logo():
    """创建一个简单的示例Logo用于演示"""
    from PIL import Image, ImageDraw
    
    # 创建一个简单的圆形Logo
    logo_size = 100
    logo = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    
    # 绘制蓝色圆形背景
    draw.ellipse((10, 10, logo_size-10, logo_size-10), fill='#4A90E2')
    
    # 绘制白色文字 "CQ"
    try:
        from PIL import ImageFont
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 36)
    except:
        # 如果找不到字体，使用默认字体
        font = ImageFont.load_default()
    
    # 计算文字位置使其居中
    text = "CQ"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (logo_size - text_width) // 2
    text_y = (logo_size - text_height) // 2
    
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    logo.save('sample_logo.png')
    return 'sample_logo.png'


def circle_dots_example():
    """圆形码点示例"""
    print("生成圆形码点二维码...")
    
    qr = CoolQRCode(
        fill_color="#FF6B6B",  # 珊瑚红
        back_color="#F8F9FA",  # 淡灰色
        error_correction=ERROR_CORRECT_H
    )
    qr.add_data("https://github.com/xxk59/cool-qrcode - 圆形码点示例")
    
    # 生成圆形码点的二维码
    img = qr.make_custom_image(size=600, dot_shape="circle")
    img.save("circle_dots_qrcode.png")
    print("✅ 圆形码点二维码已保存为 circle_dots_qrcode.png")


def circular_logo_example():
    """圆形Logo示例"""
    print("生成带圆形Logo的二维码...")
    
    # 创建示例Logo
    logo_path = create_sample_logo()
    
    qr = CoolQRCode(
        fill_color="#6C5CE7",  # 紫色
        back_color="white",
        box_size=12,
        border=4
    )
    qr.add_data("Cool QRCode - 圆形Logo演示")
    
    # 添加圆形Logo
    img = qr.add_logo(logo_path, size_ratio=0.25, circular=True, border_size=3)
    img.save("circular_logo_qrcode.png")
    print("✅ 圆形Logo二维码已保存为 circular_logo_qrcode.png")


def combined_features_example():
    """组合特性示例：圆形码点 + 圆形Logo"""
    print("生成圆形码点+圆形Logo的二维码...")
    
    logo_path = 'sample_logo.png'  # 使用之前创建的Logo
    
    qr = CoolQRCode(
        fill_color="#00D2D3",  # 青色
        back_color="#F7F1E3",  # 米色
        error_correction=ERROR_CORRECT_H
    )
    qr.add_data("Cool QRCode 全特性演示 - 圆形码点与圆形Logo的完美结合！")
    
    # 生成带圆形码点和圆形Logo的二维码
    img = qr.add_logo_to_custom(
        logo_path=logo_path,
        size=700,
        dot_shape="circle",
        logo_size_ratio=0.2,
        circular_logo=True
    )
    img.save("combined_features_qrcode.png")
    print("✅ 组合特性二维码已保存为 combined_features_qrcode.png")


def color_variations_example():
    """多彩样式示例"""
    print("生成多种颜色风格的二维码...")
    
    styles = [
        {"name": "ocean", "fill": "#0074D9", "back": "#E6F3FF", "desc": "海洋风格"},
        {"name": "forest", "fill": "#2ECC40", "back": "#F0FFF0", "desc": "森林风格"},
        {"name": "sunset", "fill": "#FF851B", "back": "#FFF8DC", "desc": "日落风格"},
        {"name": "night", "fill": "#B10DC9", "back": "#F5F5F5", "desc": "夜空风格"}
    ]
    
    for style in styles:
        qr = CoolQRCode(
            fill_color=style["fill"],
            back_color=style["back"],
            error_correction=ERROR_CORRECT_H
        )
        qr.add_data(f"Cool QRCode - {style['desc']}")
        
        # 生成圆形码点版本
        img = qr.make_custom_image(size=400, dot_shape="circle")
        img.save(f"{style['name']}_style_qrcode.png")
        print(f"✅ {style['desc']}二维码已保存为 {style['name']}_style_qrcode.png")


def high_resolution_example():
    """高分辨率示例"""
    print("生成高分辨率二维码...")
    
    qr = CoolQRCode(
        fill_color="black",
        back_color="white",
        error_correction=ERROR_CORRECT_H
    )
    
    data = """
    Cool QRCode 高分辨率演示
    
    特性：
    • 自定义码点形状（方形/圆形）
    • 圆形Logo支持
    • 高质量渲染
    • 灵活的尺寸控制
    • 丰富的颜色选项
    
    项目地址：https://github.com/xxk59/cool-qrcode
    """
    
    qr.add_data(data.strip())
    
    # 生成高分辨率图像
    img = qr.make_custom_image(size=1000, dot_shape="square")
    img.save("high_resolution_qrcode.png")
    print("✅ 高分辨率二维码已保存为 high_resolution_qrcode.png")


def cleanup():
    """清理临时文件"""
    temp_files = ['sample_logo.png']
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 已清理临时文件: {file}")


def main():
    """主函数"""
    print("🌟 Cool QRCode 高级特性演示")
    print("=" * 50)
    
    try:
        circle_dots_example()
        print()
        
        circular_logo_example()
        print()
        
        combined_features_example()
        print()
        
        color_variations_example()
        print()
        
        high_resolution_example()
        print()
        
        print("🎉 所有高级特性演示完成！")
        print("请查看生成的各种风格二维码图片文件。")
        print()
        print("新特性说明：")
        print("📍 圆形码点 - 让二维码看起来更柔和现代")
        print("📍 圆形Logo - 自动将Logo处理成圆形效果")
        print("📍 自定义尺寸 - 精确控制输出图像大小")
        print("📍 高质量渲染 - 逐个像素绘制，质量更高")
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")
    finally:
        cleanup()


if __name__ == "__main__":
    main() 