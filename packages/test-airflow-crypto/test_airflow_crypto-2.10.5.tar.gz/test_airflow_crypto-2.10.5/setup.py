from setuptools import setup, find_packages

version="2.10.5"

setup(
    name='test-airflow-crypto',
    version=version,
    packages=find_packages(),
    # author="Dataflow",
    # description="Airflow customized for Dataflow",
    install_requires=[
        'cryptography==44.0.3',
        f'apache-airflow=={version}',
        'apache-airflow-providers-postgres==6.0.0',
        'apache-airflow-providers-amazon==9.2.0',
        'apache-airflow-providers-cncf-kubernetes==10.1.0',
        'eval_type_backport'
    ],
    package_data={
        'airflow': [
            'www/static/**/*',
            "www/templates/**/*",
        ]
    },
    include_package_data=True,
    # url="https://github.com/Digital-Back-Office/dataflow-airflow"    
)