from setuptools import setup, find_packages

setup(
    name='zaheeruddin',
    version='0.1.0',
    description='Personal and professional profile module of Mohd Zaheeruddin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mohd Zaheeruddin',
    author_email='info.zaheerjk@gmail.com',
    url='https://github.com/mdzaheerjk/zaheerjk',  # Use your GitHub repo if public
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='zaheerjk profile education ai ml',
)
