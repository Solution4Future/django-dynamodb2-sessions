from setuptools import setup, find_packages
import dynamodb2_sessions

long_description = open('README.rst').read()

major_ver, minor_ver = dynamodb2_sessions.__version__
version_str = '%d.%d' % (major_ver, minor_ver)

setup(
    name='django-dynamodb2-sessions',
    version=version_str,
    packages=find_packages(),
    description="Sessions backend dedicated for Django uses Amazon DynamoDB v.2",
    long_description=long_description,
    author='Justyna Zarna',
    author_email='justyna.zarna@solution4future.com',
    license='BSD License',
    url='https://github.com/Solution4Future/django-dynamodb2-sessions',
    platforms=["any"],
    install_requires=['django', "boto>=2.10.0"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
