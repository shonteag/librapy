from distutils.core import setup


setup(
	name="librapy",
	author="Shonte Amato-Grill",
	author_email="shonte.amatogrill@gmail.com",
	package_dirs={'': 'src'},
	entry_points = {
		'console_scripts': ['librapy=src.__main__:main']
	}
)