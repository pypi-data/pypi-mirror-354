from setuptools import setup, Extension

# 定义扩展模块
module = Extension(
    'example',  # 模块名称
    sources=['example.c']  # 源代码文件
)

# 设置模块
setup(
    name='example',
    version='1.0',
    description='Example module written in C',
    ext_modules=[module]
)