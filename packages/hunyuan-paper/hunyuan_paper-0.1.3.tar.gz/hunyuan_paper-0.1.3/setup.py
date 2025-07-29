from setuptools import setup, find_packages

str_version = '0.1.3'

setup(name='hunyuan-paper',
      version=str_version,
      description='Hunyuan Paper',
      author='YuanqiMcp',
      author_email='yuanqi_mcp@tencent.com',
      license_text='MIT',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            # 定义命令行工具，用户运行 uvx your-mcp-server 时会执行 your_mcp_server.main:main
            'hunyuan-paper=hunyuan_paper.main:run_mcp',
        ],
      },
      zip_safe=False,
      include_package_data=True,
      install_requires=['mcp', 'httpx', 'uvicorn'],
      python_requires='>=3.10')
