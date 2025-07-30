from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

# ✅ Dependencies define karo yahaan
requires = [
    "pyrogram",
    "tgcrypto",
    "pymongo",
    "dnspython",
    # Add other dependencies here
]

setup(
    name="AuthNex",
    version="1.1",
    packages=find_packages(),
    install_requires=requires,
    author="Kuro__",
    author_email="sufyan532011@gmail.com",
    description="just a try",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/RyomenSukuna53/AuthNex",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
