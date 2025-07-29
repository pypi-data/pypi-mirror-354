import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "wasend",
    "version": "1.3.0",
    "description": "Wasend SDK for multiple programming languages",
    "license": "Apache-2.0",
    "url": "https://wasend.dev",
    "long_description_content_type": "text/markdown",
    "author": "Wasend<admin@wasend.dev>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/wasenddev/wasend-sdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "wasend",
        "wasend._jsii"
    ],
    "package_data": {
        "wasend._jsii": [
            "core@1.3.0.jsii.tgz"
        ],
        "wasend": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "jsii>=1.112.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
