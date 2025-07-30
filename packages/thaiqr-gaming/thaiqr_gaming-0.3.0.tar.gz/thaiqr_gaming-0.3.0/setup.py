import setuptools

import thaiqrpayment

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thaiqr-gaming",
    version=thaiqrpayment.__VERSION__,
    author="Kittinan Srithaworn",
    description="Thai QR Payment Generator with Gaming Features and Anti-Fraud Security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=["qrcode", "pillow", "crc16"],
    keywords="Thai QR Payment Generator Gaming Anti-Fraud Security Watermark",
    url="https://github.com/kittinan/thai-qr-payment",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Reports": "https://github.com/kittinan/thai-qr-payment/issues",
        "Source": "https://github.com/kittinan/thai-qr-payment",
    },
    python_requires=">=3.6",
)
