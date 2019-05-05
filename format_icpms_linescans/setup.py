import setuptools

setuptools.setup(
    name="format_icpms_linescans",
    version="1.0.1",
    author="David Kuter",
    author_email="david.kuter@gmail.com",
    description="Tool to format LA-ICP-MS data",
    long_description="Formats LA-ICP-MS line-scan csv files into separate elemental matrix files",
    url="https://github.com/davidkuter/ICP-MS/tree/master/",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={'console_scripts': ['format_icpms_linescans = format_icpms_linescans:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use  ",
        "Operating System :: Unix  ",
    ],
)
