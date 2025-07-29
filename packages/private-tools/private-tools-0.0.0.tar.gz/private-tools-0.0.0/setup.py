
from setuptools import setup
# 公開用パッケージの作成 [ezpip]
import ezpip

# 公開用パッケージの作成 [ezpip]
with ezpip.packager(develop_dir = "./_develop_private_tools/") as p:
	setup(
		name = "private-tools",
		version = "0.0.0",
		description = "A support tool for loading custom tools (easily adds the directory of the import source)",
		author = "bib_inf",
		author_email = "contact.bibinf@gmail.com",
		url = "https://github.co.jp/",
		packages = p.packages,
		install_requires = ["ezpip", "relpath>=3.0.5", "fies>=1.5.0"],
		long_description = p.long_description,
		long_description_content_type = "text/markdown",
		license = "CC0 v1.0",
		classifiers = [
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries",
			"License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
		],
		# entry_points = """
		# 	[console_scripts]
		# 	py6 = py6:console_command
		# """
	)
