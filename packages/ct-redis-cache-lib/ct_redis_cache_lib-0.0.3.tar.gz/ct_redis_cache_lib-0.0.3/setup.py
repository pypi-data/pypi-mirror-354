from setuptools import find_packages, setup

setup(
    name='ct-redis-cache-lib',
    packages=find_packages(),
    version='0.0.3',  # Increment version
    description='A specialized library developed by Credenti for efficient Redis caching in Flask applications.',
    long_description=open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    author='credenti',
    author_email='mgude@credenti.io',
    install_requires=["redis==5.2.0", "Flask>=3.0.3"],
)
