import distutils.cygwinccompiler
from distutils.version import LooseVersion
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


# 修复 MSVC 版本检测
def patch_get_msvcr():
    original_get_msvcr = distutils.cygwinccompiler.get_msvcr

    def patched_get_msvcr():
        try:
            return original_get_msvcr()
        except ValueError:
            # 使用 MinGW 的运行时库替代 MSVC 的
            return ['msvcrt']  # MinGW 对应的 C 运行时库

    distutils.cygwinccompiler.get_msvcr = patched_get_msvcr


# 应用补丁
patch_get_msvcr()


# 自定义 build_ext 命令，移除对 msvcr140 的依赖
class CustomBuildExt(build_ext):
    def build_extensions(self):
        # 移除链接选项中的 -lmsvcr140
        for ext in self.extensions:
            if hasattr(ext, 'libraries') and 'msvcr140' in ext.libraries:
                ext.libraries.remove('msvcr140')
                # 添加 MinGW 的运行时库
                if 'msvcrt' not in ext.libraries:
                    ext.libraries.append('msvcrt')

        build_ext.build_extensions(self)

# 继续执行原始的 setup.py 逻辑
if __name__ == "__main__":
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