from setuptools import setup, find_packages

setup(
    name="nonebot-plugin-nobleduel",
    version="0.2.0",
    packages=find_packages(),
    description="一个基于NoneBot2的贵族决斗插件",
    author="ATRI",
    author_email="2058550737@qq.com",
    url="https://github.com/yourusername/nonebot-plugin-nobleduel",
    install_requires=[
        "nonebot2>=2.0.0",
        "nonebot-adapter-onebot>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 