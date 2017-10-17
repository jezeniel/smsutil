from setuptools import setup
from smsutil.__version__ import VERSION

with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = [
    'future==0.16.0'
]

test_requirements = [
    'pytest'
]

setup_requirements = [
    'pytest-runner'
]

setup(
    name='smsutil',
    version=VERSION,
    description='encode, decode and split SMS.',
    long_description=readme,
    author='Jezeniel Zapanta',
    author_email='jezeniel.zapanta@gmail.com',
    url='https://github.com/jezeniel/smsutil',
    license='MIT',
    packages=['smsutil'],
    keywords='sms utils utilities smsutil short message service',
    install_requires=requirements,
    # test_requires=test_requirements,
    setup_requires=setup_requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ]
)
