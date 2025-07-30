#!/usr/bin/env python3
"""
Cool QRCode 万能函数示例
展示 make_cool_qrcode() 的所有功能和组合效果
"""

from cool_qrcode import make_cool_qrcode, create_sample_logo

print("🌟 Cool QRCode 万能函数演示")
print("=" * 50)


def demo_1_basic():
    """演示1: 最基础的使用"""
    print("📱 最基础的使用...")
    
    # 最简单 - 只需要文字
    make_cool_qrcode("Hello World!")
    
    # 保存到文件
    make_cool_qrcode("我的第一个二维码", filename="基础二维码.png")


def demo_2_colors():
    """演示2: 颜色设置"""
    print("🎨 颜色设置演示...")
    
    # 自定义颜色
    make_cool_qrcode(
        "自定义颜色",
        colors=("red", "pink"),
        filename="红色二维码.png"
    )
    
    # 预设风格
    make_cool_qrcode(
        "海洋风格",
        style="ocean",
        filename="海洋风格.png"
    )
    
    # 不同风格展示
    styles = ["forest", "sunset", "berry", "fire"]
    for style in styles:
        make_cool_qrcode(
            f"{style}风格很棒",
            style=style,
            filename=f"{style}风格.png"
        )


def demo_3_shapes():
    """演示3: 形状变化"""
    print("🔘 形状变化演示...")
    
    # 方形码点
    make_cool_qrcode(
        "方形码点",
        style="mint",
        dot_shape="square",
        filename="方形码点.png"
    )
    
    # 圆形码点
    make_cool_qrcode(
        "圆形码点",
        style="mint",
        dot_shape="circle",
        filename="圆形码点.png"
    )


def demo_4_logos():
    """演示4: Logo效果"""
    print("🖼️ Logo效果演示...")
    
    # 创建示例Logo
    logo_path = create_sample_logo("demo_logo.png")
    
    # 基础Logo
    make_cool_qrcode(
        "带Logo的二维码",
        logo_path=logo_path,
        filename="基础Logo.png"
    )
    
    # 圆形Logo + 彩色
    make_cool_qrcode(
        "圆形Logo",
        style="berry",
        logo_path=logo_path,
        logo_circular=True,
        filename="圆形Logo.png"
    )
    
    # 方形Logo + 圆形码点
    make_cool_qrcode(
        "方形Logo圆形码点",
        colors=("darkgreen", "lightgreen"),
        dot_shape="circle",
        logo_path=logo_path,
        logo_circular=False,
        filename="方形Logo圆形码点.png"
    )


def demo_5_masks():
    """演示5: 蒙板效果"""
    print("🎭 蒙板效果演示...")
    
    # 基础蒙板
    make_cool_qrcode(
        "蓝色蒙板",
        mask_color="blue",
        mask_opacity=0.3,
        filename="蓝色蒙板.png"
    )
    
    # 不同透明度
    opacities = [0.2, 0.4, 0.6]
    for opacity in opacities:
        make_cool_qrcode(
            f"透明度{opacity}",
            mask_color="red",
            mask_opacity=opacity,
            filename=f"透明度{opacity}.png"
        )


def demo_6_combinations():
    """演示6: 组合效果"""
    print("🚀 组合效果演示...")
    
    logo_path = "demo_logo.png"  # 使用之前创建的Logo
    
    # 组合1: 风格 + 圆形码点
    make_cool_qrcode(
        "组合1: 风格+圆点",
        style="sunset",
        dot_shape="circle",
        filename="组合1.png"
    )
    
    # 组合2: 颜色 + Logo + 圆形码点
    make_cool_qrcode(
        "组合2: 颜色+Logo+圆点",
        colors=("purple", "lavender"),
        dot_shape="circle",
        logo_path=logo_path,
        filename="组合2.png"
    )
    
    # 组合3: 风格 + 蒙板
    make_cool_qrcode(
        "组合3: 风格+蒙板",
        style="forest",
        mask_color="green",
        mask_opacity=0.2,
        filename="组合3.png"
    )
    
    # 组合4: 所有效果！
    make_cool_qrcode(
        "终极组合: 包含所有特效的超级二维码！",
        style="night",
        dot_shape="circle",
        logo_path=logo_path,
        logo_circular=True,
        mask_color="purple",
        mask_opacity=0.15,
        size=600,
        filename="终极组合.png"
    )


def demo_7_sizes():
    """演示7: 不同尺寸"""
    print("📏 尺寸变化演示...")
    
    sizes = [300, 500, 800]
    for size in sizes:
        make_cool_qrcode(
            f"尺寸{size}像素",
            style="chocolate",
            dot_shape="circle",
            size=size,
            filename=f"尺寸{size}.png"
        )


def demo_8_practical_examples():
    """演示8: 实用示例"""
    print("💼 实用示例演示...")
    
    # 网址二维码
    make_cool_qrcode(
        "https://github.com/xxk59/cool-qrcode",
        style="ocean",
        dot_shape="circle",
        filename="项目网址.png"
    )
    
    # 联系信息
    contact_info = """
    姓名: 小明
    电话: 138-0000-0000
    邮箱: xiaoming@example.com
    学校: XX小学
    班级: 三年级2班
    """
    make_cool_qrcode(
        contact_info.strip(),
        style="berry",
        dot_shape="circle",
        size=500,
        filename="联系信息.png"
    )
    
    # 座右铭
    make_cool_qrcode(
        "好好学习，天天向上！💪",
        style="fire",
        dot_shape="circle",
        mask_color="orange",
        mask_opacity=0.1,
        filename="座右铭.png"
    )


def show_summary():
    """显示总结"""
    print("\n🎉 万能函数演示完成！")
    print("\n💡 make_cool_qrcode() 万能函数特点:")
    print("• 一个函数搞定所有需求")
    print("• 支持自由组合各种效果")
    print("• 参数清晰，易于理解")
    print("• 可以从简单到复杂逐步学习")
    
    print("\n📚 参数说明:")
    print("• text: 二维码内容（必需）")
    print("• filename: 保存文件名")
    print("• size: 图片大小")
    print("• colors: 自定义颜色 (前景色, 背景色)")
    print("• style: 预设风格 ocean/forest/sunset/berry/fire/mint/chocolate/night")
    print("• dot_shape: 码点形状 square/circle")
    print("• logo_path: Logo文件路径")
    print("• logo_circular: Logo是否圆形")
    print("• mask_color: 蒙板颜色")
    print("• mask_opacity: 蒙板透明度 (0.0-1.0)")
    
    print("\n🌟 推荐学习路径:")
    print("1. 从最简单开始: make_cool_qrcode('Hello!')")
    print("2. 尝试预设风格: make_cool_qrcode('Hello!', style='ocean')")
    print("3. 添加圆形码点: make_cool_qrcode('Hello!', style='ocean', dot_shape='circle')")
    print("4. 组合更多效果...")


def main():
    """主函数"""
    try:
        demo_1_basic()
        print()
        
        demo_2_colors()
        print()
        
        demo_3_shapes()
        print()
        
        demo_4_logos()
        print()
        
        demo_5_masks()
        print()
        
        demo_6_combinations()
        print()
        
        demo_7_sizes()
        print()
        
        demo_8_practical_examples()
        print()
        
        show_summary()
        
    except Exception as e:
        print(f"❌ 出现错误: {e}")
        print("💬 请检查代码和文件路径")


if __name__ == "__main__":
    main() 