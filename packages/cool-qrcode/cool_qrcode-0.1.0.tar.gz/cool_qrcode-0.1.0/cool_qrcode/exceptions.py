"""
异常处理模块
"""


class CoolQRCodeError(Exception):
    """Cool QRCode的基础异常类"""
    pass


class InvalidDataError(CoolQRCodeError):
    """无效数据异常"""
    pass


class InvalidLogoError(CoolQRCodeError):
    """无效Logo异常"""
    pass


class ImageGenerationError(CoolQRCodeError):
    """图像生成异常"""
    pass 