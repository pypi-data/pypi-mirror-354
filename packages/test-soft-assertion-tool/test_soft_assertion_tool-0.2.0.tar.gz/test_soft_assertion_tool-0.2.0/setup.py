from setuptools import setup, find_packages

setup(
    name="test_soft_assertion_tool",
    version="0.2.0",
    description="A pytest plugin for soft assertions with automatic report.",
    author="WYK",
    packages=find_packages(),
    install_requires=[
        "loguru",
        "pytest",
    ],
    entry_points={
        "pytest11": [
            "assertion = assertion.pytest_softassert",
        ],
    },
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
