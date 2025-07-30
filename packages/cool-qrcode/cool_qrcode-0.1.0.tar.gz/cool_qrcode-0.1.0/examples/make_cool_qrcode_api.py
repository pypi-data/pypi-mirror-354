#!/usr/bin/env python3
"""
make_cool_qrcode API示例
演示Cool QRCode库万能函数的使用方法

注意: 所有函数的'text'参数已更名为'data'参数以与qrcode库保持一致，
但为了保持向后兼容性，可以直接传递字符串作为第一个位置参数。
"""

from cool_qrcode import make_cool_qrcode, create_sample_logo
import os


def basic_examples():
    """基础用法示例"""
    print("=== 基础用法示例 ===")
    
    # 示例1: 最基本用法 - 只提供内容
    # 默认大小为500x500像素，方形码点，黑白色
    # 注: 第一个参数是data (二维码内容)
    qr1 = make_cool_qrcode("https://github.com/xxk59/cool-qrcode")
    qr1.save("basic_qr.png")
    print("✓ 已生成基本二维码: basic_qr.png")
    
    # 示例2: 保存到文件
    # 如果提供filename参数，会自动保存文件
    make_cool_qrcode(
        "这是自动保存的二维码",  # data参数
        filename="auto_saved.png"
    )
    print("✓ 已自动保存二维码: auto_saved.png")
    
    # 示例3: 自定义大小
    # size参数控制图像尺寸，默认为500
    make_cool_qrcode(
        "大尺寸二维码",  # data参数
        size=800,
        filename="large_qr.png"
    )
    print("✓ 已生成大尺寸二维码: large_qr.png")
    
    print()


def color_examples():
    """颜色用法示例"""
    print("=== 颜色用法示例 ===")
    
    # 示例1: 自定义颜色
    # 使用fill_color和back_color参数设置前景色和背景色
    make_cool_qrcode(
        "自定义颜色二维码",
        fill_color="blue",
        back_color="lightblue",
        filename="custom_colors.png"
    )
    print("✓ 已生成自定义颜色二维码: custom_colors.png")
    
    # 示例2: 使用十六进制颜色代码
    # 可以使用#RRGGBB格式的十六进制颜色代码
    make_cool_qrcode(
        "十六进制颜色二维码",
        fill_color="#FF6B6B",
        back_color="#F8F9FA",
        filename="hex_colors.png"
    )
    print("✓ 已生成十六进制颜色二维码: hex_colors.png")
    
    # 示例3: 使用预设风格
    # style参数使用预设的颜色组合
    for style in ["ocean", "forest", "sunset", "berry"]:
        make_cool_qrcode(
            f"{style}风格二维码",
            style=style,
            filename=f"{style}_style.png"
        )
        print(f"✓ 已生成{style}风格二维码: {style}_style.png")
    
    print()


def shape_examples():
    """形状用法示例"""
    print("=== 形状用法示例 ===")
    
    # 示例1: 方形码点(默认)
    make_cool_qrcode(
        "方形码点二维码",
        dot_shape="square",
        fill_color="red",
        back_color="white",
        filename="square_dots.png"
    )
    print("✓ 已生成方形码点二维码: square_dots.png")
    
    # 示例2: 圆形码点
    make_cool_qrcode(
        "圆形码点二维码",
        dot_shape="circle",
        fill_color="green",
        back_color="white",
        filename="circle_dots.png"
    )
    print("✓ 已生成圆形码点二维码: circle_dots.png")
    
    print()


def logo_examples():
    """Logo用法示例"""
    print("=== Logo用法示例 ===")
    
    # 创建示例Logo
    logo_path = create_sample_logo("demo_logo.png")
    print(f"✓ 已创建示例Logo: {logo_path}")
    
    # 示例1: 添加圆形Logo(默认)
    make_cool_qrcode(
        "圆形Logo二维码",
        logo_path=logo_path,
        logo_circular=True,
        filename="circular_logo.png"
    )
    print("✓ 已生成圆形Logo二维码: circular_logo.png")
    
    # 示例2: 添加方形Logo
    make_cool_qrcode(
        "方形Logo二维码",
        logo_path=logo_path,
        logo_circular=False,
        filename="square_logo.png"
    )
    print("✓ 已生成方形Logo二维码: square_logo.png")
    
    print()


def mask_examples():
    """蒙板用法示例"""
    print("=== 蒙板用法示例 ===")
    
    # 示例1: 添加蓝色蒙板
    make_cool_qrcode(
        "蓝色蒙板二维码",
        mask_color="blue",
        mask_opacity=0.3,  # 默认透明度
        filename="blue_mask.png"
    )
    print("✓ 已生成蓝色蒙板二维码: blue_mask.png")
    
    # 示例2: 不同透明度蒙板
    for opacity in [0.1, 0.3, 0.5, 0.7]:
        make_cool_qrcode(
            f"透明度{opacity}的蒙板",
            mask_color="purple",
            mask_opacity=opacity,
            filename=f"mask_opacity_{opacity}.png"
        )
        print(f"✓ 已生成透明度{opacity}的蒙板二维码: mask_opacity_{opacity}.png")
    
    print()


def combination_examples():
    """组合效果示例"""
    print("=== 组合效果示例 ===")
    
    logo_path = "demo_logo.png"  # 使用之前创建的Logo
    
    # 示例1: 风格 + 圆形码点
    make_cool_qrcode(
        "风格+圆形码点",
        style="ocean",
        dot_shape="circle",
        filename="style_circle.png"
    )
    print("✓ 已生成风格+圆形码点二维码: style_circle.png")
    
    # 示例2: 风格 + Logo
    make_cool_qrcode(
        "风格+Logo",
        style="sunset",
        logo_path=logo_path,
        filename="style_logo.png"
    )
    print("✓ 已生成风格+Logo二维码: style_logo.png")
    
    # 示例3: 圆形码点 + Logo + 蒙板
    make_cool_qrcode(
        "圆点+Logo+蒙板",
        fill_color="darkblue",
        back_color="white",
        dot_shape="circle",
        logo_path=logo_path,
        mask_color="blue",
        mask_opacity=0.2,
        filename="circle_logo_mask.png"
    )
    print("✓ 已生成圆点+Logo+蒙板二维码: circle_logo_mask.png")
    
    # 示例4: 所有效果组合
    make_cool_qrcode(
        "所有效果组合示例",
        style="berry",        # 使用预设风格
        dot_shape="circle",   # 圆形码点
        logo_path=logo_path,  # 添加Logo
        logo_circular=True,   # 圆形Logo
        mask_color="purple",  # 紫色蒙板
        mask_opacity=0.15,    # 透明度
        size=600,             # 大尺寸
        filename="all_features.png"
    )
    print("✓ 已生成所有效果组合二维码: all_features.png")
    
    print()


def main():
    """主函数"""
    print("🌟 make_cool_qrcode API 示例")
    print("=" * 40)
    print("这个示例演示了make_cool_qrcode函数的所有用法")
    print()
    
    # 创建输出目录
    output_dir = "make_cool_qrcode_examples"
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)
    print(f"所有示例将保存在 {output_dir} 目录下")
    print()
    
    # 运行各类示例
    basic_examples()
    color_examples()
    shape_examples()
    logo_examples()
    mask_examples()
    combination_examples()
    
    print("🎉 所有示例完成！")
    print(f"请查看 {output_dir} 目录下的图片文件")


if __name__ == "__main__":
    main() 