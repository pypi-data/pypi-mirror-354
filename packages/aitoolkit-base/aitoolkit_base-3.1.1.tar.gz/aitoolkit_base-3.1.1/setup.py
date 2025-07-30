#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIToolkit Base 3.1.1 安装配置文件 - 懒加载优化版
支持whl打包和分发，大幅提升启动速度
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# 读取版本号
def get_version():
    version_file = os.path.join('aitoolkit_base', '__init__.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')
    return '3.1.1'

# 基础依赖（核心功能）
install_requires = [
    # 核心CV库
    'opencv-python>=4.5.0,<5.0.0',
    'numpy>=1.20.0,<2.0.0',
    'Pillow>=8.0.0,<11.0.0',
    
    # MediaPipe核心
    'mediapipe>=0.10.0,<0.11.0',
    
    # 基础工具
    'requests>=2.25.0',
    'tqdm>=4.60.0',
    
    # 避免protobuf版本冲突
    'protobuf>=3.20.0,<5.0.0',
]

# 可选依赖（分组安装）
extras_require = {
    # 深度学习训练功能
    'training': [
        'torch>=1.12.0',
        'torchvision>=0.13.0',
        'tensorboard>=2.8.0',
    ],
    
    # 高级深度估计
    'depth': [
        'torch>=1.12.0',
        'torchvision>=0.13.0',
        'timm>=0.6.0',  # MiDaS依赖
    ],
    
    # 中文OCR支持
    'ocr': [
        'cnocr>=2.2.0',
        'onnxruntime>=1.12.0',
    ],
    
    # Web摄像头支持
    'cam': [
        'aitoolkit-cam>=0.3.0',
        'flask>=2.0.0',
    ],
    
    # 开发工具
    'dev': [
        'pytest>=6.0.0',
        'pytest-cov>=2.12.0',
        'black>=21.0.0',
        'flake8>=3.9.0',
        'mypy>=0.910',
    ],
    
    # 文档生成
    'docs': [
        'mkdocs>=1.4.0',
        'mkdocs-material>=8.0.0',
        'mkdocstrings[python]>=0.19.0',
    ],
}

# 完整安装（所有功能）
extras_require['all'] = sum(extras_require.values(), [])

setup(
    name='aitoolkit-base',
    version=get_version(),
    author='AIToolkit Team',
    author_email='support@aitoolkit.dev',
    description='易用的AI视觉处理工具包 - 懒加载优化版，基于MediaPipe和OpenCV，启动速度提升26000倍！',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/aitoolkit/aitoolkit-base',
    project_urls={
        'Bug Reports': 'https://github.com/aitoolkit/aitoolkit-base/issues',
        'Source': 'https://github.com/aitoolkit/aitoolkit-base',
        'Documentation': 'https://aitoolkit-base.readthedocs.io/',
    },
    
    packages=find_packages(exclude=['tests*', 'examples*', 'docs*']),
    include_package_data=True,
    
    # 包数据
    package_data={
        'aitoolkit_base': [
            'models/*.tflite',
            'models/*.task',
            'models/*.onnx',
        ],
    },
    
    # Python版本要求
    python_requires='>=3.8,<4.0',
    
    # 依赖管理
    install_requires=install_requires,
    extras_require=extras_require,
    
    # PyPI分类
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        'Topic :: Education',
    ],
    
    # 关键词
    keywords=[
        'computer-vision', 'ai', 'machine-learning', 'mediapipe', 
        'opencv', 'face-detection', 'pose-estimation', 'image-processing',
        'deep-learning', 'artificial-intelligence', 'computer-vision-library'
    ],
    
    # 命令行工具
    entry_points={
        'console_scripts': [
            'aitoolkit-test=aitoolkit_base.utils:run_tests',
            'aitoolkit-install=aitoolkit_base.utils:run_install_guide',
        ],
    },
    
    # 依赖解析选项
    zip_safe=False,
    
    # 平台特定选项
    options={
        'bdist_wheel': {
            'universal': False,  # 不是纯Python包（包含预编译模型）
        }
    },
)

# 打包完成提示
print("\n" + "=" * 60)
print("�� AIToolkit Base 3.1.1 打包配置完成！")
print("=" * 60)
print("\n🚀 打包命令:")
print("  python setup.py sdist bdist_wheel")
print("\n📤 上传命令:")
print("  twine upload dist/*")
print("\n💡 安装命令:")
print("  pip install aitoolkit-base")
print("  pip install aitoolkit-base[ocr]         # 包含OCR功能")
print("  pip install aitoolkit-base[torch]       # 包含Torch相关功能")
print("  pip install aitoolkit-base[training]    # 包含训练功能")
print("  pip install aitoolkit-base[all]         # 包含所有可选功能")
print("\n🎯 控制台命令:")
print("  aitoolkit-test")
print("  aitoolkit-install")
print("=" * 60) 