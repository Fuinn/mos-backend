from setuptools import setup, find_packages

setup(name='mos-backend',
      zip_safe=False,
      version='0.1.0',
      author='Fuinn',
      url='https://github.com/Fuinn/mos-backend',
      description='MOS Backend',
      license='Apache License, Version 2.0',
      packages=find_packages(),
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3.6'])
