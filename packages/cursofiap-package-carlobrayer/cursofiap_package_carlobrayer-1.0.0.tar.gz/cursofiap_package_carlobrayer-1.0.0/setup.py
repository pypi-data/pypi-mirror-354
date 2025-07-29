from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='cursofiap_package_carlobrayer',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='Carlo Brayer',
    author_email='carlobrayer@gmail.com',
    url='https://github.com/carlobrayer/cursofiap',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
