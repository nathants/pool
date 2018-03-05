import setuptools


setuptools.setup(
    version="0.0.1",
    license='mit',
    name='py-pool',
    python_requires='>=3.6',
    author='nathan todd-stone',
    author_email='me@nathants.com',
    url='http://github.com/nathants/py-pool',
    packages=['pool'],
    install_requires=['py-util'],
    dependency_links=['https://github.com/nathants/py-util/tarball/4d1fe20ecfc0b6982933a8c9b622b1b86da2be5e#egg=py-util-0.0.1'],
    description='process and thread pools',
)
