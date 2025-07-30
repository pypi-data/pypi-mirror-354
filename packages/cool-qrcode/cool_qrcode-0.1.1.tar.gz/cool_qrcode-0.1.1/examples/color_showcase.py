#!/usr/bin/env python3
"""
Cool QRCode 颜色展示
展示所有支持的颜色
"""

from cool_qrcode import make_cool_qrcode

# 基础颜色
BASIC_COLORS = [
    "red", "green", "blue", "yellow", "purple", 
    "orange", "pink", "cyan", "black", "white",
    "gray", "grey"
]

# 常用颜色
COMMON_COLORS = [
    "aqua", "black", "blue", "fuchsia", "grey", "lime", 
    "maroon", "navy", "olive", "purple", "red", "silver", 
    "teal", "white", "yellow", "orange"
]

# 扩展颜色
EXTENDED_COLORS = [
    "lightblue", "lightgreen", "lightcyan", "lightyellow",
    "lavender", "lightgray", "lightpink", "darkblue",
    "darkgreen", "darkorange", "darkred", "brown", "wheat"
]


def showcase_colors(colors, prefix, dot_shape="square"):
    """展示一组颜色"""
    print(f"\n展示{prefix}颜色 ({len(colors)}种)...")
    
    for color in colors:
        # 使用白色背景使颜色更明显
        filename = f"{prefix}_{color}.png"
        
        # 生成二维码
        make_cool_qrcode(
            f"{color}",
            colors=(color, "white"),
            dot_shape=dot_shape,
            filename=filename
        )
        
        print(f"✓ 已生成 {color} 颜色的二维码")


def main():
    """主函数"""
    print("🎨 Cool QRCode 颜色展示")
    print("=" * 40)
    
    try:
        # 展示基础颜色
        showcase_colors(BASIC_COLORS, "基础", dot_shape="square")
        
        # 展示常用颜色
        showcase_colors(COMMON_COLORS, "常用", dot_shape="circle")
        
        # 展示扩展颜色
        showcase_colors(EXTENDED_COLORS, "扩展", dot_shape="square")
        
        print("\n🎉 所有颜色展示完成！")
        print(f"共展示了 {len(BASIC_COLORS) + len(COMMON_COLORS) + len(EXTENDED_COLORS)} 种颜色")
        print("请查看生成的PNG文件以了解每种颜色的效果")
        
    except Exception as e:
        print(f"❌ 出现错误: {e}")


if __name__ == "__main__":
    main() 