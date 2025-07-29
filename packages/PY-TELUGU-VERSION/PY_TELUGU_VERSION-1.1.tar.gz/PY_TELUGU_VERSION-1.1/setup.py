from setuptools import setup, find_packages

setup(
    name="PY_TELUGU_VERSION",
    version="1.1",
    packages=find_packages(),
    include_package_data=True,
      package_data={
        "PY_TELUGU_VERSION": ["keywords_te.json"],
    },
    entry_points={
        'console_scripts': [
            'pythontel = PY_TELUGU_VERSION.auto_update:main',
            'pythonrun = PY_TELUGU_VERSION.main:main',
        ],
    },
    author="sunstromium",
    description="literal telugu package for python programming",
    long_description="this package convert the english keywords in python to telugu , i am currently using json file to convert them, it is lot of pain to every single word so it takes times to complete this project ",
    long_description_content_type="text/plain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
