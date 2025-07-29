from setuptools import setup, find_packages
setup(
    name='jenkins_kit',
    version='0.1.6',
    packages=find_packages(),
    authors=[{'name':'hrcodes','email':'thusharamurikinati887@gmail.com'}],
    description = ("A Python Library for Jenkins Pipelines creation."),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Topic :: Utilities",
    ],
    install_requires=['python-jenkins==1.8.2','chevron==0.14.0']
)