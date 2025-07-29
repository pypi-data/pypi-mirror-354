import os, setuptools, sys, numpy as np

this_folder = os.path.abspath(os.path.dirname(__file__))
parent_folder = os.path.abspath(os.path.join(this_folder, '..'))
python_include_folder = os.path.abspath(os.path.join(sys.executable, 'include'))
numpy_include_folder = np.get_include()


with open(os.path.join(this_folder, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '2025.6.8'    # OPEN: read from VERSION file


setuptools.setup(
    name='bones-kernel',
    url = 'https://github.com/coppertop-bones/bones-kernel',
    version=VERSION,
    install_requires=[
        'numpy >= 1.17.3'
    ],
    ext_modules=[
        setuptools.Extension(
            'bones.jones',
            sources=[
                'src/jones/mod_jones.c'
            ],
            include_dirs=[
                python_include_folder,
                numpy_include_folder,
            ],
        ),
    ],
    # packages=setuptools.find_packages(where='src'),
    # package_dir={'': 'src'},
    python_requires='>=3.11',
    license='OSI Approved :: Apache Software License',
    description='Jones - the bones kernel for coppertop',
    long_description_content_type='text/markdown',
    long_description='Jones - the bones kernel for coppertop',
    author='David Briant',
    author_email = 'dangermouseb@forwarding.cc',
    download_url = '',
    keywords=[
        'multiple', 'dispatch', 'piping', 'pipeline', 'pipe', 'functional', 'multimethods', 'multidispatch',
        'functools', 'lambda', 'curry', 'currying'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.11',
    ],
)

