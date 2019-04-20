import setuptools

setuptools.setup(
    name="format_icpms_map_data",
    version="1.0.0",
    author="David Kuter",
    author_email="david.kuter@gmail.com",
    description="Tool to format LA-ICP-MS data",
    long_description="Formats LA-ICP-MS csv files into separate elemental matrix files for 2D contour plotting",
    url="https://github.com/davidkuter/ICP-MS/tree/master/",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={'console_scripts': ['format_icpms_map_data = format_icpms_map_data:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use  ",
        "Operating System :: Unix  ",
    ],
)
