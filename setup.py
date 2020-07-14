import os
import io

from setuptools import setup


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

about = {}
with io.open(os.path.join(BASE_DIR, 'smsutil', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)


requirements = [
    'future>=0.16.0'
]

test_requirements = [
    'pytest==4.6.*'
]

setup_requirements = [
    'pytest-runner'
]

setup(
    name='smsutil',
    version=about['__version__'],
    description='encode, decode and split SMS.',
    long_description=readme,
    author='Jezeniel Zapanta',
    author_email='jezeniel.zapanta@gmail.com',
    url='https://github.com/jezeniel/smsutil',
    license='MIT',
    packages=['smsutil'],
    keywords='sms utils utilities smsutil short message service',
    install_requires=requirements,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ]
)
