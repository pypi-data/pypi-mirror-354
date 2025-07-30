from setuptools import setup, find_packages

with open("README.md" , "r" , encoding="utf-8")as fh:
    long_description = fh.read()

setup(
    name="nonebot-plugin-nobleduel",
    version="0.1.0",
    description="一个贵族决斗小游戏插件",
    author="cikasaaa",
    author_email="2058550737@qq.com", 
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "nonebot2>=2.0.0",
        "nonebot-adapter-onebot>=2.0.0",
        "nonebot-plugin-alconna>=0.7.0",
        "nonebot-plugin-apscheduler>=0.2.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Games/Entertainment",
    ],
    url="https://github.com/cikasaaa/nonebot-plugin-NobleDuel",
)