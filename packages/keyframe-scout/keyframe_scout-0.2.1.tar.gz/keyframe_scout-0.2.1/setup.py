from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="keyframe-scout",
    version="0.2.1",  # 更新版本号
    author="Jiajun Chen",
    author_email="cjj198909@gmail.com",
    description="Intelligent video keyframe extraction tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/keyframe-scout",
    
    # 关键：添加这行来包含 Python 包
    packages=find_packages(),  # 这会自动找到 keyframe_scout 目录
    # 或者明确指定：
    # packages=['keyframe_scout'],
    
    include_package_data=True,  # 包含 MANIFEST.in 中指定的文件
    
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "Pillow>=8.0.0",
        "tqdm>=4.50.0",
        "scikit-image>=0.18.0",
    ],
    
    extras_require={
        'azure': [
            'openai>=1.0.0',
        ],
        'dev': [
            'pytest>=6.0',
            'black',
            'flake8',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'keyframe-scout=keyframe_scout.__main__:main',
            'keyframe-scout-batch=keyframe_scout.batch:batch_main',
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    python_requires=">=3.7",
)