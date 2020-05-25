import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "sdswatch",
  version = "0.0.1",
  packages = setuptools.find_packages(),
  author = "David Tran",
  author_email = "vitrandao@gmail.com",
  description = "SDS Watch",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  python_requires = '>=3.0',
)

  
