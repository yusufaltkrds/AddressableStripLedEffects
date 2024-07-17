from setuptools import setup, find_packages

setup(
    name='LED',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'rpi_ws281x',
    ],
    entry_points={
        'console_scripts': [
            'LED=LED.main:main',
        ],
    },
    author='Muhammed Yusuf Altikardes',
    author_email='yusufaltkrds123@gmail.com',
    description='Controlling Led strip with different effects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/kullanıcı_adı/project_name',
    python_requires='>=3.9',
)
