import pathlib
from setuptools import setup, find_packages # type: ignore

# Get the long description from README.md
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name='django-dynamic-maintenance-mode',
    version='0.1.0',
    description='Django middleware to enable maintenance mode dynamically using a database flag.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Pranav Dixit',
    author_email='pranavdixit20@gmail.com',
    url='https://github.com/pranav-dixit/django-dynamic-maintenance-mode',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=[
        'Django>=3.2',
    ],
    entry_points={
        'console_scripts': [
            # Optional: future CLI commands
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.7',
)