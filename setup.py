from setuptools import setup, find_packages

setup(
    name='graph_nous',
    version='0.1.0',
    description='Sistema híbrido de ETL e visualização de grafos RDF e Neo4j de dados públicos',
    author='Ronen Filho',
    author_email='ronen.filho@gmail.com',
    url='https://github.com/ronenfilho/graph_nous',
    packages=find_packages(include=['graph', 'graph.*']),
    include_package_data=True,
    install_requires=[
        # Evite listar aqui. Prefira requirements.txt
    ],
    python_requires='>=3.11',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
