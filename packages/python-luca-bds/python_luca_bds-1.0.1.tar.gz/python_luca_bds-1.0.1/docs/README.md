# LUCA BDS

[LUCA BDS](https://luca-bds.com/) is a business intelligence platform designed to centralize access to all your company's information, empowering users with real-time data analysis and visualization tools for informed decision-making. This library provides a set of tools for interacting with the [LUCA BDS](https://luca-bds.com/) API. It allows you to perform queries and execute operations in the LUCA environment using secure connections.

## Installation

You can install the library via PyPI. Make sure to have Python installed on your machine, then run:

```bash
pip install python-luca-bds
```

## Usage

Below is an example of how to use the LUCA BDS client to connect to the server and test some functionality:

```python
from luca.connectors import LucaConnector
from luca.querys import query

# LUCA connection configuration
luca_conn = LucaConnector(
    server_url='https://luca-bds-domain/luca-api',
    username='user',
    password='pass'
)

# Retrieve connection information
info = luca_conn.info()
print(info)

# Execute a query by name
result, pag, state = query(
    conn=luca_conn,
    name='Prueba',
    environment='DES'
)
print(result)

# Execute a query by ID
result, pag, state = query(
    conn=luca_conn,
    id=364,
    environment='DES',
    input_variables=[{'Usuario': 'luca', 'Sistema': 'LUCA'}]
)
print(result)
print(pag)
print(state)
```