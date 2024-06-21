from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return lines


setup(
    name="Stop-signal-task",
    description="TODO description",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/thatmariia/stop-signal-task",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        'console_scripts': [
            'py_experiment = experiment:experiment',
            'py_image_generation = image_generation:image_generation',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.10"
        # "License :: X,
    ],
    python_requires="==3.10.*"
)