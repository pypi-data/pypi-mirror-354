from setuptools import setup

setup(
    name='DXR',
    version='2.1.10',
    packages=['Dxr_mqtt', 'Dxr_log', 'Dxr_bytes', 'Dxr_utils', 'Dxr_video', 'Dxr_serial', 'Dxr_yaml', 'Dxr_file', 'Dxr_grpc', 'Dxr_isapi', 'Dxr_voice', 'Dxr_Chat', 'Dxr_redis', 'dxr_cli', 'Dxr_file_async', 'Dxr_Crypto'],
    package_data={
        'Dxr_Crypto': ['lib/**/*', 'QuantumUKey/**/*'],
    },
    install_requires=['paho-mqtt', 'pyyaml', 'pyserial', 'loguru','tabulate', 'pymysql', 'sqlalchemy', 'oss2', 'imagezmq', 'simplejpeg', 'pexpect', 'aiortsp', 'click', 'tiktoken', 'prompt_toolkit', 'openai', 'rich', 'fastapi', 'uvicorn', 'psutil'],
    author='luzhipeng',
    author_email='402087139@qq.com',
    license='MIT',
    url='http://pycn.me',
    description='DXR is a python library for DXR_mqtt',
    entry_points={
        'console_scripts': [
            'dxr=dxr_cli.cli:dxr',
        ],
    },
)
