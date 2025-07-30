from setuptools import setup, find_packages

setup(
    name="astrbot_plugin_create_meme",
    version="0.0.5",
    description="一个用于 astrbot 的宝藏袋插件",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xiaomizhoubaobei/astrbot_plugin_create_meme",
    author="祁筱欣",  # Replace with your name
    author_email="mzapi@x.mizhoubaobei.top",  # Replace with your email
    packages=find_packages(),
    py_modules=["main", "emoji"],
    include_package_data=True,
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    project_urls={
        "Homepage": "https://github.com/xiaomizhoubaobei/astrbot_plugin_create_meme",
        "Download": "https://github.com/xiaomizhoubaobei/astrbot_plugin_create_meme/releases",
        "Issues": "https://github.com/xiaomizhoubaobei/astrbot_plugin_create_meme/issues",
        "Bug": "https://github.com/xiaomizhoubaobei/astrbot_plugin_create_meme/issues",
        "GitHub": "https://github.com/xiaomizhoubaobei/astrbot_plugin_create_meme",
        "Twitter": "https://x.com/XinXiao12088",
        "Pypi": "https://pypi.org/project/astrbot_plugin_treasure_create_meme/",
    },
)
