from setuptools import setup, find_packages

setup(
    name='auto-doc-gen',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pipreqs',
        'chardet',
        'gitignore_parser'
    ],
    entry_points={
        'console_scripts': [
            'autodoc=main:main',
        ],
    },
    author='Kimie JIN',
    author_email='szweiforwork@example.com',
    description='自動產生 README、.gitignore 與 requirements.txt 的 CLI 工具',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/szweijin/auto_doc_gen.git',
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
