from setuptools import setup, find_packages

setup(
    name='pyoptparse',
    version="0.1",
    url='http://github.com/SpaceKookie/OptionsPie/',
    license='GNU Public Liense 2.0',
    author='Katharina Sabel',
    author_email='katharina.sabel@2rsoftworks.de',
    description='Python commandline argument parser',
    packages=['src'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    # package_data={
    #     'poke': ['controllers/**']
    # }
)
