from setuptools import setup, find_packages

name = 'html_parsing_dqa'
version = '0.1.0'
install_requires = [
    're',
    'bs4',
]


setup(
    name = name,
    version = version,
    # url = 'https://code.devops.xiaohongshu.com/jinlei1/mmidls',
    author = 'jinqiu',
    author_email = 'jinqiu@xiaohongshu.com',
    description = 'utils for html parsing',
    packages = find_packages(),
    zip_safe = True,
    include_package_data = True,
    install_requires = install_requires,
)

