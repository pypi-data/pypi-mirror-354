from setuptools import setup, find_packages

setup(
    name='ros-pointcloud-recorder',
    version='0.1.3',
    packages=find_packages(),
    description='ROS Point Cloud Recorder and Exporter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='knighthood2001',
    author_email='2109695291@qq.com',
    url='https://github.com/Knighthood2001/ros-pointcloud-recorder',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    keywords='ros pointcloud recorder pcl rosbag lidar',
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8'
        ]
    },
    entry_points={
        'console_scripts': [
            'ros-pcd-recorder=ros_pointcloud_recorder.cli:main',
        ],
    },
)