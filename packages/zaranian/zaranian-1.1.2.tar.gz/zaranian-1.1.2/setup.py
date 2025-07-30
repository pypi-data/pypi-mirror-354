# setup.py
from setuptools import setup
from setuptools.command.install import install
import sys

class CustomInstallCommand(install):
    def run(self):
        try:
            from zaranian import show_popup
            show_popup()
        except Exception as e:
            print("失敗:", e)
        install.run(self)

setup(
    name='zaranian',
    version='1.1.2',
    description='ramを割り当ててvramにするユーティリティパッケージ windowsのみ対応',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='グラファイト',
    author_email='gymk@gaypan.com',
    url='https://github.com/zakogarisuki2/zaranian',
    packages=['zaranian'],
    cmdclass={
        'install': CustomInstallCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
