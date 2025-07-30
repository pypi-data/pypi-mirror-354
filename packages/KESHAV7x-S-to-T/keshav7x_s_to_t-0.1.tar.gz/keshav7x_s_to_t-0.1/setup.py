from setuptools import setup,find_packages

setup(
    name='KESHAV7x_S_to_T',
    version='0.1',
    author='Keshav',
    author_email='heyitskeshav@gmail.com',
    description='speech to text package created by keshav'
)
packages =find_packages()
install_requirement =[
    'selenium',
    'webdriver_manager'
]
