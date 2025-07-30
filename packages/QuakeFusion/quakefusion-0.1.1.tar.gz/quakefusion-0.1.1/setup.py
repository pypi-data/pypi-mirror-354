from setuptools import setup

setup(
    name="QuakeFusion",
    version="0.1.1",
    long_description="quakefusion",
    long_description_content_type="text/markdown",
    packages=["quakefusion"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)
