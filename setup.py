from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vpnium',
  version='1.0.1',
  description='Python library for managing a VPN extension for Chrome WebDriver',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/d3kxrma/vpnium',
  project_urls={
      "Source": "https://github.com/d3kxrma/vpnium"
  },
  author='dekxrma',
  author_email='qqdjnuxez@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='python, selenium, vpn, proxy',
  packages=find_packages(),
  install_requires=['requests', 'chrome-version', 'selenium'] 
)