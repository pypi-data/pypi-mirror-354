from setuptools import setup, find_packages

setup(
    name="paros_data_grabber",
    version="0.1.1",
    author="Ethan Gelfand",
    author_email="egelfand@umass.edu",
    description="A package to query Parosbox InfluxDB data securely",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["paros_data_grabber", "paros_data_grabber.*"]),
    package_data={
        "paros_data_grabber.creds": ["influx-creds.enc"],  # include your encrypted creds
    },
    include_package_data=True,
    install_requires=[
        "influxdb-client",
        "pandas",
        "scipy",
        "cryptography",
        "pytz",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
