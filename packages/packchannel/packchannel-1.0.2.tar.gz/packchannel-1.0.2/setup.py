import setuptools


def read_requirements():
    with open('requirements.txt', 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return requirements


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="packchannel",
    version="1.0.2",
    author="lining",
    author_email="58633102@qq.com",
    description="A tool channel test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    package_data={
        'channel': ['**/*'],  # 递归包含channel下所有文件
    },
    data_files=[
        ('', ['requirements.txt', 'main.py', 'README.md']),  # 包含根目录文件
    ],
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'ug-build=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
