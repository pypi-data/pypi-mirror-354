from setuptools import setup, find_packages
import os

# Function to read the long description from README.md
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return 'A downloader application for Kemono and Coomer sites.'

setup(
    name='yuvi-downloader', # The name of your package on PyPI
    version='5.0.1',       # Increment this for new releases
    author='Yuvi',         # Your name or your GitHub username
    author_email='your_email@example.com', # Optional: your email
    description='A downloader application for Kemono and Coomer sites.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/Yuvi9587/Kemono-Downloader-Public', # Your project's URL
    
    # find_packages() will automatically find your 'yuvi' package.
    # We also specify where to find the 'assets' and other data.
    packages=find_packages(include=['yuvi', 'yuvi.*']),
    
    # This tells setuptools to include files specified in MANIFEST.in
    include_package_data=True, 
    
    # List your project's dependencies
    install_requires=[
        'PyQt5>=5.15',
        'requests>=2.20',
        'Pillow>=8.0', 
        'mega.py>=1.0.8', # For Mega downloads
        'gdown>=4.0.0',   # For Google Drive downloads
        'setuptools'      # Ensures setuptools is available
    ],
    
    # This creates a command-line script to run your application
    entry_points={
        'gui_scripts': [
            'yuvi-downloader=yuvi.main:main_cli', 
        ],
    },
    
    # Classifiers help users find your project
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License', # Choose your license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Environment :: X11 Applications :: Qt',
    ],
    python_requires='>=3.8',
)
