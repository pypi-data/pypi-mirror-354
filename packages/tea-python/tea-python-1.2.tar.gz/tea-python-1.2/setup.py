from setuptools import setup, find_packages

file_path = 'README.md'

setup(name='tea-python',
      version='1.2',
      description='Tiny Encryption Algorithm',
      long_description=open(file_path, encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      author="luckpi",
      author_email="ojbk@live.com",
      url="https://github.com/luckpi/tea-python",
      packages=find_packages(),
      data_files=[file_path],
      classifiers=(
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ))
