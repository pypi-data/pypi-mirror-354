import argparse
import sys

import setuptools

# 添加 argparse 参数解析
parser = argparse.ArgumentParser()
parser.add_argument("--dev", action="store_true", help="Use development version instead of VERSION file")
args, unknown = parser.parse_known_args()
# 修改 sys.argv 以确保 setuptools 不报错（因为它也会解析命令行参数）
sys.argv = [sys.argv[0]] + unknown

# 选择版本号
if args.dev:
    version = "0.0.0.dev0"
else:
    with open("VERSION", "r", encoding="utf-8") as f:
        version = f.read().strip()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open-ttg",
    version=version,
    author="monkitect.com",
    author_email="1304646911@qq.com",
    description="graph builder from text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monkitect/text2graph.git",
    project_urls={
        "Bug Tracker": "https://github.com/monkitect/text2graph/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    test_suite="nose.collector",
    tests_require=["nose"],
    python_requires=">=3.6",
    install_requires=['jieba'],
)
