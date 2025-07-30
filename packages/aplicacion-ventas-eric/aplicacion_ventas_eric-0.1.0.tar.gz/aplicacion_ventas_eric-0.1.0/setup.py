from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="aplicacion_ventas_eric",
    version="0.1.0",
    author="DlsRage",
    author_email='spc525nc1@gmail.com',
    description="Paquete para gestionar ventas, precios, impuestos y descuentos",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com/curso_python_camara/gestor/aplicacionventas',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
