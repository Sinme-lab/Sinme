from setuptools import setup, find_packages

setup(
    name="sinme",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "web3",
        "torch",
        "fastapi",
        "pydantic",
        "eth-account",
        "python-multipart",
        "uvicorn",
        "sqlalchemy",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "cryptography",
    ],
    author="Sinme Team",
    author_email="contact@sinme.io",
    description="A decentralized AI model training platform using blockchain technology",
    keywords="blockchain, AI, federated learning, decentralized",
) 