"""Setup tool for DLWMLS."""

from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="DLWMLS",
    version="0.1.0",
    description="DLWMLS - Deep Learning White Matter Lesion Segmentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kyunglok Baik, Yuhan Cui, Guray Erus",
    author_email="software@cbica.upenn.edu",
    maintainer="Kyunglok Baik",
    maintainer_email="kyunglok.baik@pennmedicine.upenn.edu",
    download_url="https://github.com/CBICA/DLWMLS/",
    url="https://github.com/CBICA/DLWMLS/",
    packages=find_packages(exclude=["tests", ".github"]),
    python_requires=">=3.9",
    install_requires=[
        "torch<=2.3.1",
        "nnunetv2<=2.5.1",
        "argparse",
        "huggingface_hub",
        "pathlib",
    ],
    entry_points={"console_scripts": ["DLWMLS = DLWMLS.__main__:main"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    license="By installing/using DLWMLS, the user agrees to the following license: See https://www.med.upenn.edu/cbica/software-agreement-non-commercial.html",
    keywords=[
        "deep learning",
        "image segmentation",
        "semantic segmentation",
        "medical image analysis",
        "medical image segmentation",
        "nnU-Net",
        "nnunet",
        "nnunetv2",
    ],
    package_data={"DLWMLS": ["VERSION"]},
)
