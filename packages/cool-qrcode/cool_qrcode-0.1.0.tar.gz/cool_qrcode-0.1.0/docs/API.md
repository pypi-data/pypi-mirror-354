# Cool QRCode API 文档

本文档详细说明了 Cool QRCode 库的 API 接口。

## 核心API

### make_cool_qrcode()

这是 Cool QRCode 库的核心函数，支持所有功能特性的组合使用。

```python
make_cool_qrcode(
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
) -> Image.Image
```

#### 参数说明

- **data** (str): 
  - 二维码内容，必须非空。可以是网址、文本、联系信息等。

- **filename** (str, 可选): 
  - 保存文件名。如果提供，二维码会保存到该文件。默认为None，不保存文件。

- **size** (int, 可选): 
  - 图片大小（像素）。默认为500像素。

- **fill_color** (str, 可选): 
  - 前景色（码点颜色），默认为"black"。
  - 可使用颜色名称或十六进制颜色代码("#FF5733")。
  - 当同时指定颜色和style时，style优先。

- **back_color** (str, 可选): 
  - 背景色，默认为"white"。
  - 可使用颜色名称或十六进制颜色代码("#F8F9FA")。
  - 当同时指定颜色和style时，style优先。

- **style** (str, 可选): 
  - 预设风格，可选值: "ocean", "forest", "sunset", "berry", "fire", "mint", "chocolate", "night"。
  - 当同时指定颜色和style时，style优先。

- **dot_shape** (str, 可选): 
  - 码点形状。可选值: "square"(方形) 或 "circle"(圆形)。默认为"square"。

- **logo_path** (str, 可选): 
  - Logo图片路径。如果提供，会在二维码中央添加Logo。默认为None。

- **logo_circular** (bool, 可选): 
  - Logo是否为圆形。如果为True，Logo会被裁剪成圆形。默认为True。

- **mask_color** (str, 可选): 
  - 蒙板颜色。如果提供，会添加半透明蒙板效果。默认为None。

- **mask_opacity** (float, 可选): 
  - 蒙板透明度，范围0.0-1.0。0.0为完全透明，1.0为完全不透明。默认为0.3。

#### 返回值

- **PIL.Image.Image**: 生成的二维码图像对象

#### 用法示例

```python
from cool_qrcode import make_cool_qrcode

# 基本用法
img = make_cool_qrcode("Hello, World!")

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
```

## 简化API

以下是针对特定用例优化的简化API函数。

### make_qrcode()

生成基本二维码 - 最简单的方式。

```python
make_qrcode(
    data: str,
    filename: Optional[str] = None,
    size: int = 500,
    fill_color: str = "black",
    back_color: str = "white",
    dot_shape: Literal["square", "circle"] = "square"
) -> Image.Image
```

#### 参数

- **data**: 二维码内容
- **filename**: 保存文件名（可选）
- **size**: 图片大小（像素）
- **fill_color**: 前景色（码点颜色）
- **back_color**: 背景色
- **dot_shape**: 码点形状 "square"(方形) 或 "circle"(圆形)

#### 示例

```python
from cool_qrcode import make_qrcode

# 最简单的用法
make_qrcode("Hello World!")

# 保存到文件
make_qrcode("Hello World!", filename="my_qr.png")

# 彩色二维码
make_qrcode("Hello World!", fill_color="red", back_color="yellow")

# 圆形码点
make_qrcode("Hello World!", dot_shape="circle")
```

### make_colorful_qrcode()

生成彩色二维码。

```python
make_colorful_qrcode(
    data: str,
    fill_color: str = "blue",
    back_color: str = "lightblue",
    filename: Optional[str] = None,
    size: int = 500,
    dot_shape: Literal["square", "circle"] = "square"
) -> Image.Image
```

#### 参数

- **data**: 二维码内容
- **fill_color**: 前景色（码点颜色）
- **back_color**: 背景色
- **filename**: 保存文件名（可选）
- **size**: 图片大小
- **dot_shape**: 码点形状

#### 示例

```python
from cool_qrcode import make_colorful_qrcode

# 蓝色二维码
make_colorful_qrcode("Hello!", "blue", "lightblue")

# 红色圆点二维码
make_colorful_qrcode("Hello!", "red", "pink", dot_shape="circle")
```

### make_qrcode_with_logo()

生成带Logo的二维码。

```python
make_qrcode_with_logo(
    data: str,
    logo_path: str,
    filename: Optional[str] = None,
    size: int = 500,
    fill_color: str = "black",
    back_color: str = "white",
    dot_shape: Literal["square", "circle"] = "square",
    logo_circular: bool = True
) -> Image.Image
```

#### 参数

- **data**: 二维码内容
- **logo_path**: Logo图片文件路径
- **filename**: 保存文件名（可选）
- **size**: 图片大小
- **fill_color**: 前景色（码点颜色）
- **back_color**: 背景色
- **dot_shape**: 码点形状
- **logo_circular**: Logo是否为圆形

#### 示例

```python
from cool_qrcode import make_qrcode_with_logo

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
```

### make_qrcode_with_mask()

生成带半透明蒙板的二维码。

```python
make_qrcode_with_mask(
    data: str,
    mask_color: str = "blue",
    mask_opacity: float = 0.3,
    filename: Optional[str] = None,
    size: int = 500,
    fill_color: str = "black",
    back_color: str = "white",
    dot_shape: Literal["square", "circle"] = "square"
) -> Image.Image
```

#### 参数

- **data**: 二维码内容
- **mask_color**: 蒙板颜色
- **mask_opacity**: 蒙板透明度 (0.0-1.0, 0完全透明，1完全不透明)
- **filename**: 保存文件名（可选）
- **size**: 图片大小
- **fill_color**: 前景色（码点颜色）
- **back_color**: 背景色
- **dot_shape**: 码点形状

#### 示例

```python
from cool_qrcode import make_qrcode_with_mask

# 蓝色半透明蒙板
make_qrcode_with_mask("Hello!", "blue", 0.3)

# 红色蒙板圆点二维码
make_qrcode_with_mask(
    "Hello!", 
    mask_color="red", 
    mask_opacity=0.4,
    dot_shape="circle"
)
```

### make_pretty_qrcode()

使用预设的漂亮颜色生成二维码。

```python
make_pretty_qrcode(
    data: str,
    style: str = "ocean",
    filename: Optional[str] = None,
    size: int = 500,
    dot_shape: Literal["square", "circle"] = "circle"
) -> Image.Image
```

#### 参数

- **data**: 二维码内容
- **style**: 颜色风格，可选: "ocean", "forest", "sunset", "berry", "fire", "mint", "chocolate", "night"
- **filename**: 保存文件名（可选）
- **size**: 图片大小
- **dot_shape**: 码点形状

#### 示例

```python
from cool_qrcode import make_pretty_qrcode

# 海洋风格
make_pretty_qrcode("Hello!", "ocean")

# 浆果风格圆点
make_pretty_qrcode("Hello!", "berry", dot_shape="circle")
```

### create_sample_logo()

创建一个示例Logo文件供练习使用。

```python
create_sample_logo(filename: str = "sample_logo.png") -> str
```

#### 参数

- **filename**: Logo文件名

#### 返回值

- 创建的Logo文件路径

#### 示例

```python
from cool_qrcode import create_sample_logo, make_qrcode_with_logo

# 创建示例Logo
logo_path = create_sample_logo()
make_qrcode_with_logo("Hello!", logo_path)
```

## 常量

### PRETTY_COLORS

预设的漂亮颜色组合。

```python
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
```

## 高级用法

对于需要更多控制的高级用户，可以直接使用核心类 `CoolQRCode`：

```python
from cool_qrcode import CoolQRCode

# 创建自定义实例
qr = CoolQRCode(
    version=1,
    error_correction="M",
    box_size=10,
    border=4,
    fill_color="black",
    back_color="white"
)

# 添加数据
qr.add_data("https://example.com")

# 生成基本图像
img = qr.make_image()

# 或生成自定义图像
img = qr.make_custom_image(size=500, dot_shape="circle")

# 添加Logo
img = qr.add_logo_to_custom(
    logo_path="logo.png",
    size=500,
    dot_shape="circle",
    logo_size_ratio=0.2,
    circular_logo=True
)

# 保存
img.save("advanced_qr.png")
``` 