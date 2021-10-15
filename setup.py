import setuptools

setuptools.setup(
    name="Pelago Reddit",
    packages=['pelago_reddit'],
    install_requires=[
        "praw",
        "psycopg2-binary",
    ],
)
