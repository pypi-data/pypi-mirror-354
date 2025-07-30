from setuptools import setup, find_packages

setup(
    name='MultiDown',
    version='0.1.0',
    description='A stylish cross-platform video downloader with web UI',
    author='Bismoy Ghosh',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'yt-dlp',
        'rich',
        'colorama',
        'ffmpeg-python'
    ],
    entry_points={
        'console_scripts': [
            'MultiDown = MultiDown.__main__:main',
        ],
    },
)
