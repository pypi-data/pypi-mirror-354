import setuptools

long_description: str

with open("README.md", "r", encoding="utf-8") as readme_file_desc:
    long_description = readme_file_desc.read()
    
setuptools.setup(
  name = 'rilz',
  packages = [
    'rilz',
    'rilz/vault',
    'rilz/encoders',
    'rilz/enums',
    'rilz/browser',
  ],
  version = '11.0.7',
  license='BSD-3-Clause',
  description = 'Rilz is an open-source self-hosted backend server that abstract and simplify complex and repetitive development tasks behind a very simple REST API',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Rilz Team',
  author_email = 'team@rilck.com',
  maintainer = 'Rilz Team',
  maintainer_email = 'team@rilck.com',
  url = 'https://rilck.com/support',
  download_url='https://github.com/rilckztech/rilz-sdk/archive/11.0.7.tar.gz',
  install_requires=[
    'requests',
    'loguru',
    'webdriver-manager',
    'selenium',
    'hvac',
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Environment :: Web Environment',
    'Topic :: Software Development',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
