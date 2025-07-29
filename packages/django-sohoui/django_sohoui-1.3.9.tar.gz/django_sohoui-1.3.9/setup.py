from setuptools import setup, find_packages

setup(
    name='django_sohoui',  # 包的名称
    version='1.3.9',  # 包的版本
    packages=find_packages(),  # 自动找到包
    install_requires=[
        'django==4.2.21',
    ],  # 依赖的其他包
    author='zack_liu',  # 作者
    author_email='liu.zhimin.2019@gmail.com',  # 作者邮箱
    description='django soho ui base',  # 简短描述
    long_description=open('README.md').read(),  # 详细描述
    long_description_content_type='text/markdown',  # 描述格式
    url='https://github.com/liuzhimin2019/django_sohoui.git',  # 项目网址
    classifiers=[  # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    python_requires='>=3',  # Python 版本要求
    django_version='4.2.21',
)
