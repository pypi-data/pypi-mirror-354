from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="patent-extractor",
    version="0.2.0",
    author="pyxist2020",
    author_email="info@pyxist.co.jp",
    description="特許PDFからマルチモーダル生成AIを使用して構造化JSONを抽出するライブラリ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyxist2020/patent-extractor",
    download_url="https://github.com/pyxist2020/patent-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Markup",
    ],
    licence="MIT",
    python_requires=">=3.8",
    install_requires=[
        "google-generativeai>=0.3.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
    ],
    entry_points={
        "console_scripts": [
            "patent-extractor=patent_extractor.patent_extractor:main",
        ],
    },
)
