from distutils.core import setup

setup(
    name='Scarsdale',
    version='0.1.0',
    packages=['scarsdale', ],
    license='Apache 2.0',
    author='Will Mitchell',
    author_email='will.mitchell@app3.com',
    long_description=open('README.md').read(),
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Semantics',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
    keywords='smart contracts semantic web schema',
)
