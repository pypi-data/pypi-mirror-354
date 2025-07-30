from setuptools import setup
import setuptools



setup(
    name='text_clean123',
    version ='0.0.1',
    description='Remove special charecters, email, urls in text',
    author= [{ "name":"Narendra sompalle", "email":"nsompalle@gmail.com" }],
    packages=setuptools.find_packages(),
    keywords=['text clean', 'url clean', 'email clean',"special charecter clean"],
    classifiers=[
        "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=['text_clean'],
    package_dir={'':'src'},
    license = "MIT",
)