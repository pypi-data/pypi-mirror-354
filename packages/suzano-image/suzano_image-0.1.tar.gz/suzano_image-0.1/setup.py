from setuptools import setup, find_packages

setup(
    name='suzano_image',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy'
    ],
    author='Seu Nome',
    description='Pacote de processamento de imagens do Bootcamp da Suzano',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
