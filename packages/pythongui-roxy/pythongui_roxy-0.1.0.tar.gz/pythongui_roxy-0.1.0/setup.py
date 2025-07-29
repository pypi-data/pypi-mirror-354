
from setuptools import setup

setup(
    name='pythongui_roxy',
    version='0.1.0',
    py_modules=['GUI', 'IK', 'dataset', 'main', 'Matix', 'ML', 'Params', 'realtest', 'test'],  
    package_data={
        '': ['*.ui', '*.jpg', '*.csv', '*.h5']  # 리소스 파일들
    },
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'scipy',
        'torch',
        'PyQt5'
    ],
    entry_points={
        'console_scripts': [
            'pythongui = GUI:main' 
        ]
    }
)
