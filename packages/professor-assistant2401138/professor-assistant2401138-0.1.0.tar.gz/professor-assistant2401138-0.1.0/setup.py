from setuptools import setup, find_packages

setup(
    name="professor-assistant2401138",  # Package name
    version="0.1.0",  # Package version
    packages=find_packages(),  # Automatically find the packages
    install_requires=[  # List of dependencies (if any)
        # 'requests',  # Example
    ],
    entry_points={
        "console_scripts": [
            "professor-assistant=professor_assistant2401138.main:main",  # Main function for command line
        ],
    },
    include_package_data=True,  # Include any non-Python files
    author="sabin",
    author_email="sabin@dsu.ac.kr",
    description="Professor Assistant Package to create exams from question banks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # For Markdown support in PyPI
  
    classifiers=[  # Classifiers for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
