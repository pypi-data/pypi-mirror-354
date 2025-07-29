import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QMarkdownWidget",
    version="1.0.0",
    author="KercyDing",
    author_email="dkx215417@gmail.com",  # 请修改为您的邮箱
    description="Markdown(LaTeX) rendering widgets for PyQt6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KercyDing/QMarkdownWidget",  # 请修改为您的GitHub仓库地址
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyQt6",
        "PyQt6-WebEngine",
        "markdown2",
    ],
) 