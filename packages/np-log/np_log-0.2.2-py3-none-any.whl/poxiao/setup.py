import datetime

from setuptools import setup, find_packages

# 获取当前日期和时间作为版本号
now = datetime.datetime.now()
version = f"0.{now.strftime('%y%m%d')}.{now.strftime('%H')}"
setup(
    name='poxiaoai',
    version=version,
    packages=find_packages(),
    install_requires=[
        # 如果有依赖，可以在这里列出
    ],
    description="破晓AI pip包",
    author="poxiaoai",
    author_email="liujinlin@poxiaoai.com",
)
