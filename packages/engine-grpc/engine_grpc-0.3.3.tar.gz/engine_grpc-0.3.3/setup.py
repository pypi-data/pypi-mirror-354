from setuptools import setup, find_packages

setup(
    name='engine_grpc',
    version='0.3.3',
    license='MIT',
    description='grpc pipeline interfaces',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='esun',
    author_email='esun@voteb.com',
    url='https://github.com/ImagineersHub/engine-grpc-pipeline',
    keywords=['python', 'grpc', 'unity', 'unreal'],
    packages=find_packages(),
    install_requires=[
        'grpcio==1.50.0',
        'grpcio-tools==1.50.0',
        'protobuf>=4.25.2,<5.0dev',
        'betterproto[compiler]==2.0.0b5',
        'ugrpc_pipe',
        'compipe>=0.2.3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.10'
    ]
)
