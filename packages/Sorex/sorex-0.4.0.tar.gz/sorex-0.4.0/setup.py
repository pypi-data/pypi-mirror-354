from setuptools import setup, find_packages

requirements = [
    "httpx",
    "websocket-client==1.3.1", 
    "setuptools", 
    "json_minify", 
    "six",
    "aiohttp",
    "websockets",
    "colorama"
]

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name="Sorex",
    author="Sor",
    version="0.4.0",
    description="By Sor. https://t.me/Tearedeyes",
    packages=find_packages(),
    long_description=long_description,
    install_requires=requirements,
    keywords=[
    	'ZAmino',
    	'ZAmino.fix',
        'aminoapps',
        'ZAminofix',
        'amino',
        'amino-bot',
    ],
    python_requires='>=3.6',
)
