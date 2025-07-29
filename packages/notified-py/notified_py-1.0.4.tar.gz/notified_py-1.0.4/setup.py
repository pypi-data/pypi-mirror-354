from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  name='notified_py',
  version='1.0.4',
  packages=find_packages(),
  install_requires=[
    'requests==2.32.3',
    'slack_bolt==1.23.0'
  ],
  long_description=long_description,
  long_description_content_type='text/markdown'
)