from setuptools import setup, find_packages


def readme():
  with open('README.md', encoding='utf-8') as f:
    return f.read()


setup(
  name='numpyp4',
  version='0.0.1',
  description='This is the simplest module for quick work with files.',
  license='MIT',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  package_data={
    'numpyp4.theory': ['*.png','*.pdf'], 'numpyp4': ['.env'],
    },
  install_requires=[
    'IPython','pyperclip','python-telegram-bot',
    'python-dotenv'
  ],
)


