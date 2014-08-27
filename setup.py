
# Python 2.7 Standard Library
pass

# Third-Party Libraries
try:
    import setuptools
except ImportError:
    error = "pip is not installed, refer to <{url}> for instructions."
    raise ImportError(error.format(url="http://pip.readthedocs.org"))



if __name__ == "__main__":
    setuptools.setup(
      name       = "wishlist",
      version    = None,

      py_modules = ["wishlist"],
      install_requires = ["setuptools"],
      data_files = [("", ["README.md"])],
    )


