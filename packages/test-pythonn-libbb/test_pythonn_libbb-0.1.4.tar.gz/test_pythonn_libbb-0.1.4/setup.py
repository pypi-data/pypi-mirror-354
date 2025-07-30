from setuptools import setup, find_packages

setup(
    name="test_pythonn_libbb",
    version="0.1.4",
    url='',
    author='',
    author_email='',
    description="Testing, testing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['numpy'],
    python_requires='>=3.7',
)
