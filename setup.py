from setuptools import setup, find_packages


setup(
	name="py2so",
	author="Shonte Amato-Grill",
	author_email="shonte.amatogrill@gmail.com",
	packages=find_packages(),
	package_data={'':['template/*.json']},
	entry_points = {
		'console_scripts': [
			'pyso = src.__main__:main',
		],
	}
)