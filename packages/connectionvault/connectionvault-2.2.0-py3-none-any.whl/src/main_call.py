from .connection_utility import (make_string, load_connections, choose_connection) # for local testting add src.xxxxx
from sqlalchemy import create_engine
import pandas as pd
import os
import yaml


def interactive() -> str:
    connections = load_connections()
    conn = choose_connection(connections)

    engine = create_engine(conn)
    query = input("Input your query: ")
    df = pd.read_sql_query(query, engine)
    return df


def return_string(xml_config: str) -> str:
    conn_home = os.environ.get('conn_home')
    connection_file = os.path.join(conn_home, 'connections.yaml')

    with open(connection_file, "r") as file:
        connections = yaml.safe_load(file)

    connection_detail = connections[xml_config]
    CONNECTION_STRING = make_string(connection_detail)
    return CONNECTION_STRING


def return_engine(xml_config: str):
    """
    Given a config name from connections.yaml, return a SQLAlchemy engine.
    """
    connection_url = return_string(xml_config)
    engine = create_engine(connection_url)
    return engine

if __name__ == "__main__":

    # Test for Return String
    string = return_string('pg_dlt')  # when running local the import should be like this {from src.connection_utility import make_string} or will give relative import error
    # and for pypi package {from .connection_utility import make_string} works
    print(string)


    # Test for Inetractive   {ex - select 1}
    # inter = interactive()  # when running local the import should be like this {from src.connection_utility import make_string} or will give relative import error
    # and for pypi package {from .connection_utility import make_string} works
    # print(inter)

