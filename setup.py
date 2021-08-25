from setuptools import setup

setup(name='manim-eqcolor', 
    version='0.4',
    description='Meta latex for manim equations', 
    url='https://github.com/twitwi/manim-eqcolor',
    author='@twitwi', 
    author_email='', 
    license='apache-2', 
    packages=['manim_eqcolor'],
    install_requires=
    [
        'manim'
    ],      
    zip_safe=False)
