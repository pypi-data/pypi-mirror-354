from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='qwertyuiop',
    packages=find_packages(),
    version='0.0.1',  # Increment version
    description='A specialized library developed by Credenti for efficient Redis caching in Flask applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # author='credenti',
    # author_email='mgude@credenti.io',
    install_requires=["redis==5.2.0", "Flask>=3.0.3"],
)
