from setuptools import setup, find_packages
from tinydb import TinyDB, Query

db = TinyDB('loacaldb.json')
infos = db.all()
if len(infos) == 0:
    version = '0.0.0.0'
    db.insert({'version': version})
else:
    version = db.all()[0]['version']
version = '.'.join(version.split('.')[:-1]) + '.' + str(int(version.split('.')[-1]) + 1)
db.update({'version': version})
db.close()
setup(
    name='jacksung',
    version=version,
    author='Zijiang Song',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tqdm',
        'requests',
        'pymysql',
        'pytz',
        'selenium',
        'termcolor',
        'einops',
        'rasterio',
        'netCDF4',
        'pyyaml',
        'opencv-python',
        'Pillow',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'ecnu_login = jacksung.utils.login:main',
            'watch_gpu = jacksung.utils.nvidia:main'
        ]
    }
)
