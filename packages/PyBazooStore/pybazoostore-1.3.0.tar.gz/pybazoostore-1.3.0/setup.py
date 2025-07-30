from setuptools import setup, find_packages

setup(
    name='PyBazooStore',
    version='1.3.0',
    author='MohammadReza',
    author_email='narnama.room@gmail.com',
    description='کتابخانه ای برای کار با بازواستور 🐍✨',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.5',
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    project_urls={
        'صفحه من ❤️': 'https://apicode.pythonanywhere.com/',
        'سایت اصلی 🌐' : 'https://webapp.bazoostore.ir/'
    },
)
