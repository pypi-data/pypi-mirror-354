"""
Cool QRCode核心模块
"""

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageDraw, ImageChops
import io
import numpy as np
from typing import Union, Optional, Literal
from pathlib import Path

from .exceptions import InvalidDataError, InvalidLogoError, ImageGenerationError


class CoolQRCode:
    """
    Cool QRCode主类，用于生成个性化二维码
    """
    
    def __init__(
        self,
        version: int = 1,
        error_correction: int = ERROR_CORRECT_M,
        box_size: int = 10,
        border: int = 4,
        fill_color: str = "black",
        back_color: str = "white"
    ):
        """
        初始化CoolQRCode实例
        
        Args:
            version: 二维码版本（1-40）
            error_correction: 纠错级别
            box_size: 每个小方块的像素大小
            border: 边框大小
            fill_color: 前景色
            back_color: 背景色
        """
        self.qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        self.fill_color = fill_color
        self.back_color = back_color
        self._data_added = False
    
    def add_data(self, data: Union[str, bytes]) -> None:
        """
        添加数据到二维码
        
        Args:
            data: 要编码的数据
            
        Raises:
            InvalidDataError: 当数据无效时抛出
        """
        if not data:
            raise InvalidDataError("数据不能为空")
        
        try:
            self.qr.add_data(data)
            self._data_added = True
        except Exception as e:
            raise InvalidDataError(f"添加数据失败: {str(e)}")
    
    def make_image(self, fit: bool = True) -> Image.Image:
        """
        生成二维码图像
        
        Args:
            fit: 是否自动调整二维码大小
            
        Returns:
            PIL Image对象
            
        Raises:
            ImageGenerationError: 当图像生成失败时抛出
        """
        if not self._data_added:
            raise ImageGenerationError("请先添加数据再生成图像")
        
        try:
            if fit:
                self.qr.make(fit=True)
            
            img = self.qr.make_image(
                fill_color=self.fill_color,
                back_color=self.back_color
            )
            return img
        except Exception as e:
            raise ImageGenerationError(f"生成图像失败: {str(e)}")
    
    def make_custom_image(
        self, 
        size: int = 500,
        dot_shape: Literal["square", "circle"] = "square",
        fit: bool = True
    ) -> Image.Image:
        """
        生成自定义样式的二维码图像
        
        Args:
            size: 输出图像大小（正方形）
            dot_shape: 码点形状，'square'(方形) 或 'circle'(圆形)
            fit: 是否自动调整二维码大小
            
        Returns:
            PIL Image对象
            
        Raises:
            ImageGenerationError: 当图像生成失败时抛出
        """
        if not self._data_added:
            raise ImageGenerationError("请先添加数据再生成图像")
        
        try:
            if fit:
                self.qr.make(fit=True)
            
            # 创建基础二维码图像用于获取模块信息
            base_img = self.qr.make_image(
                fill_color=self.fill_color,
                back_color=self.back_color
            ).convert('RGBA')
            
            # 创建自定义大小的图像
            img_custom = Image.new('RGBA', (size, size), self.back_color)
            draw = ImageDraw.Draw(img_custom)
            
            # 计算码点大小
            modules_count = self.qr.modules_count
            dot_size = size / (modules_count * 2)
            
            # 绘制每个模块
            for r in range(modules_count):
                for c in range(modules_count):
                    if self.qr.modules[r][c]:
                        x = c * size // modules_count + size // (2 * modules_count)
                        y = r * size // modules_count + size // (2 * modules_count)
                        
                        if dot_shape == 'circle':
                            draw.ellipse(
                                (x - dot_size, y - dot_size, x + dot_size, y + dot_size),
                                fill=self.fill_color
                            )
                        else:  # square
                            draw.rectangle(
                                (x - dot_size, y - dot_size, x + dot_size, y + dot_size),
                                fill=self.fill_color
                            )
            
            return img_custom
            
        except Exception as e:
            raise ImageGenerationError(f"生成自定义图像失败: {str(e)}")
    
    def add_logo(
        self, 
        logo_path: Union[str, Path], 
        size_ratio: float = 0.3,
        border_size: int = 2,
        circular: bool = False
    ) -> Image.Image:
        """
        在二维码中心添加Logo
        
        Args:
            logo_path: Logo文件路径
            size_ratio: Logo相对于二维码的大小比例
            border_size: Logo周围的白色边框大小
            circular: 是否将Logo处理成圆形
            
        Returns:
            带Logo的二维码图像
            
        Raises:
            InvalidLogoError: 当Logo无效时抛出
            ImageGenerationError: 当图像生成失败时抛出
        """
        # 首先生成基础二维码
        qr_img = self.make_image()
        
        # 检查logo文件
        logo_path = Path(logo_path)
        if not logo_path.exists():
            raise InvalidLogoError(f"Logo文件不存在: {logo_path}")
        
        try:
            # 打开logo图像
            logo = Image.open(logo_path).convert('RGBA')
            
            # 计算logo大小
            qr_width, qr_height = qr_img.size
            logo_size = int(min(qr_width, qr_height) * size_ratio)
            
            # 调整logo大小
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # 如果需要圆形处理
            if circular:
                # 获取logo原有alpha通道
                logo_alpha = logo.split()[-1] if logo.mode == 'RGBA' else Image.new('L', logo.size, 255)
                
                # 创建圆形遮罩
                mask = Image.new('L', (logo_size, logo_size), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, logo_size, logo_size), fill=255)
                
                # 合并原alpha和圆形遮罩
                final_alpha = ImageChops.multiply(logo_alpha, mask)
                logo.putalpha(final_alpha)
            
            # 创建带白色边框的logo
            if border_size > 0:
                bordered_size = logo_size + 2 * border_size
                if circular:
                    # 圆形边框
                    bordered_logo = Image.new('RGBA', (bordered_size, bordered_size), (0, 0, 0, 0))
                    draw_border = ImageDraw.Draw(bordered_logo)
                    draw_border.ellipse((0, 0, bordered_size, bordered_size), fill='white')
                else:
                    # 方形边框
                    bordered_logo = Image.new('RGBA', (bordered_size, bordered_size), 'white')
                
                # 计算logo在边框中的位置
                logo_pos = border_size
                bordered_logo.paste(logo, (logo_pos, logo_pos), logo)
                logo = bordered_logo
                logo_size = bordered_size
            
            # 计算logo在二维码中的位置（居中）
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            # 将logo粘贴到二维码上
            qr_img.paste(logo, logo_pos, logo if logo.mode == 'RGBA' else None)
            
            return qr_img
            
        except Exception as e:
            raise ImageGenerationError(f"添加Logo失败: {str(e)}")
    
    def add_logo_to_custom(
        self,
        logo_path: Union[str, Path],
        size: int = 500,
        dot_shape: Literal["square", "circle"] = "square",
        logo_size_ratio: float = 0.2,
        circular_logo: bool = True
    ) -> Image.Image:
        """
        在自定义样式二维码中心添加Logo
        
        Args:
            logo_path: Logo文件路径
            size: 二维码图像大小
            dot_shape: 码点形状
            logo_size_ratio: Logo大小比例
            circular_logo: 是否使用圆形Logo
            
        Returns:
            带Logo的自定义二维码图像
            
        Raises:
            InvalidLogoError: 当Logo无效时抛出
            ImageGenerationError: 当图像生成失败时抛出
        """
        # 生成自定义样式的二维码
        qr_img = self.make_custom_image(size=size, dot_shape=dot_shape)
        
        # 检查logo文件
        logo_path = Path(logo_path)
        if not logo_path.exists():
            raise InvalidLogoError(f"Logo文件不存在: {logo_path}")
        
        try:
            # 打开并处理logo
            logo_image = Image.open(logo_path).convert('RGBA')
            logo_size = int(size * logo_size_ratio)
            logo_image = logo_image.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            if circular_logo:
                # 获取logo原有alpha通道
                logo_alpha = logo_image.split()[-1]
                
                # 创建圆形遮罩
                mask = Image.new('L', (logo_size, logo_size), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, logo_size, logo_size), fill=255)
                
                # 合并原alpha和圆形遮罩
                final_alpha = ImageChops.multiply(logo_alpha, mask)
                logo_image.putalpha(final_alpha)
            
            # 将logo粘贴到二维码中心
            qr_img.paste(
                logo_image,
                ((size - logo_size) // 2, (size - logo_size) // 2),
                logo_image
            )
            
            return qr_img
            
        except Exception as e:
            raise ImageGenerationError(f"添加Logo到自定义二维码失败: {str(e)}")
    
    def save(
        self, 
        filename: Union[str, Path], 
        format: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        保存二维码图像到文件
        
        Args:
            filename: 文件名
            format: 图像格式（如果不指定，将从文件扩展名推断）
            **kwargs: 传递给PIL Image.save的其他参数
        """
        img = self.make_image()
        img.save(filename, format=format, **kwargs)
    
    def to_bytes(self, format: str = 'PNG') -> bytes:
        """
        将二维码图像转换为字节数据
        
        Args:
            format: 图像格式
            
        Returns:
            图像的字节数据
        """
        img = self.make_image()
        bio = io.BytesIO()
        img.save(bio, format=format)
        return bio.getvalue()
    
    def clear(self) -> None:
        """
        清除当前的数据，重置二维码
        """
        self.qr.clear()
        self._data_added = False 