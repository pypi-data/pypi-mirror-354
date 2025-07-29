from setuptools import setup,find_packages
import os
# 安全读取 README.md（兼容 Windows/Linux）
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except Exception as e:
    print(f"Error reading README.md: {e}")
    long_description = "ADB 工具包"  # 默认描述

setup(
    name='adb-chix',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask'
    ],
    entry_points={
        'console_scripts':[
            'adb-chix=adb_chix:run_server'
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)