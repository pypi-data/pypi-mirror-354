from setuptools import setup, find_packages

setup(
	name='lib_video_parser',
	version='1.1',
	packages=find_packages(),
	install_requires=[
		'requests',
		'beautifulsoup4',
		'fake_useragent',
		'aiohttp',
	],
	description='Library for parse video files',
	long_description=open('README.md', encoding='utf-8').read(),
	long_description_content_type="text/markdown",
	author='Yurij',
	author_email='yuran.ignatenko@yandex.ru',
	url='https://github.com/YuranIgnatenko/lib_video_parser',
)