#!/usr/bin/env python3
"""
Cool QRCode 简单使用示例 - 专为小学生设计
用最简单的方式生成各种漂亮的二维码
"""

# 方式1: 导入所有简单函数
from cool_qrcode import *

# 方式2: 只导入需要的函数
# from cool_qrcode import make_qrcode, make_colorful_qrcode, make_qrcode_with_logo

print("🎨 Cool QRCode 简单使用示例")
print("=" * 40)


def example_1_basic():
    """示例1: 最简单的二维码"""
    print("📱 生成最简单的二维码...")
    
    # 只需要一行代码！
    make_qrcode("Hello, 我是小学生制作的二维码！", filename="简单二维码.png")


def example_2_colorful():
    """示例2: 彩色二维码"""
    print("🌈 生成彩色二维码...")
    
    # 红色二维码
    make_colorful_qrcode(
        "我喜欢红色！",
        fill_color="red",
        back_color="pink",
        filename="红色二维码.png"
    )
    
    # 蓝色圆点二维码
    make_colorful_qrcode(
        "蓝色圆点很可爱",
        fill_color="blue", 
        back_color="lightblue",
        dot_shape="circle",
        filename="蓝色圆点二维码.png"
    )


def example_3_pretty_styles():
    """示例3: 使用漂亮的预设风格"""
    print("✨ 生成各种风格的二维码...")
    
    # 查看所有可用的风格
    print("可用的风格:", list(PRETTY_COLORS.keys()))
    
    # 海洋风格
    make_pretty_qrcode(
        "我喜欢大海！",
        style="ocean",
        filename="海洋风格二维码.png"
    )
    
    # 森林风格
    make_pretty_qrcode(
        "大自然真美丽",
        style="forest", 
        dot_shape="circle",
        filename="森林风格二维码.png"
    )
    
    # 浆果风格
    make_pretty_qrcode(
        "紫色是我最爱的颜色",
        style="berry",
        filename="浆果风格二维码.png"
    )


def example_4_with_logo():
    """示例4: 带Logo的二维码"""
    print("🖼️ 生成带Logo的二维码...")
    
    # 首先创建一个示例Logo
    logo_file = create_sample_logo("我的logo.png")
    
    # 生成带Logo的二维码
    make_qrcode_with_logo(
        "这是我的专属二维码！",
        logo_path=logo_file,
        colors=("purple", "lavender"),
        dot_shape="circle",
        filename="带Logo的二维码.png"
    )


def example_5_with_mask():
    """示例5: 带半透明蒙板的二维码"""
    print("🎭 生成带蒙板的二维码...")
    
    # 蓝色蒙板
    make_qrcode_with_mask(
        "半透明效果很酷！",
        mask_color="blue",
        mask_opacity=0.3,
        filename="蓝色蒙板二维码.png"
    )
    
    # 红色蒙板圆点
    make_qrcode_with_mask(
        "红色蒙板圆点",
        mask_color="red",
        mask_opacity=0.4,
        dot_shape="circle",
        filename="红色蒙板圆点二维码.png"
    )


def example_6_advanced_combo():
    """示例6: 高级组合效果"""
    print("🚀 生成组合效果二维码...")
    
    # 组合所有特效：彩色 + 圆点 + Logo + 大尺寸
    logo_file = "我的logo.png"  # 使用之前创建的Logo
    
    make_qrcode_with_logo(
        "我学会了制作超棒的二维码！包含我的姓名、班级和爱好。",
        logo_path=logo_file,
        colors=("darkorange", "lightyellow"),
        dot_shape="circle",
        size=600,
        filename="我的超棒二维码.png"
    )


def show_tips():
    """显示使用小贴士"""
    print("\n💡 小贴士:")
    print("• text参数：写你想要的文字，中文英文都可以")
    print("• filename参数：文件名，可以用中文") 
    print("• colors参数：颜色可以用英文名字，如'red', 'blue', 'green'")
    print("• dot_shape参数：'square'是方点，'circle'是圆点")
    print("• size参数：数字越大图片越大")
    print("• 用手机扫描生成的二维码，看看能不能识别你的文字！")


def main():
    """主函数"""
    try:
        example_1_basic()
        print()
        
        example_2_colorful()
        print()
        
        example_3_pretty_styles()
        print()
        
        example_4_with_logo()
        print()
        
        example_5_with_mask()
        print()
        
        example_6_advanced_combo()
        print()
        
        print("🎉 所有示例都完成了！")
        print("快去文件夹里看看你制作的二维码吧！")
        
        show_tips()
        
    except Exception as e:
        print(f"❌ 出现错误: {e}")
        print("💬 如果遇到问题，请检查你的代码是否正确")


if __name__ == "__main__":
    main() 