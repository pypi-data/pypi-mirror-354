from sqlalchemy import text
from .connection_manager import main as conn_manage_main
from .main_call import interactive
import argparse
import os
import sys

# Hardcoded version information
VERSION = "2.2.0"

# Hardcoded dependencies information
DEPENDENCIES = {
    "python": "^3.11",
    "PyYAML": "^6.0.2",
    "SQLAlchemy": "^2.0.36",
    "psycopg2": "^2.9.10",
    "pandas": "^2.2.3",
    "pyodbc": "^5.2.0",
    "pylint": "^3.3.1",
    "mysql-connector-python": "^9.3.0",
    "poetry": "^1.8.4"
}

# Hardcoded usage information
EXAMPLE = """

ENSURE YOU HAVE SET THE ENVIRONMENT VARIABLE 'conn_home' TO THE DIRECTORY WHERE YOUR connections.yaml FILE IS LOCATED.

Sample Usage 1: for batch jobs

    from .main_call import return_string
    string = return_string('pass db config name here')
    print(string)

Sample Usage 2: interactive (CLI)

    connectionvault --interactive

"""

def main():
    print(">>> ✅ Connectionvault CLI loaded")
    parser = argparse.ArgumentParser(description='ConnectionVault CLI Tool')
    parser.add_argument('--version', action='version', version=f'ConnectionVault {VERSION}')
    parser.add_argument('--dependencies', action='store_true', help='Show project dependencies')
    parser.add_argument('--example', action='store_true', help='Show sample code syntax')
    parser.add_argument('--connections', action='store_true', help='Start connection manager utility')
    parser.add_argument('--yamldir', action='store_true', help='Show location of connection.yaml file')
    parser.add_argument('--interactive', action='store_true', help='Run a SQL from CLI')
    parser.add_argument('--test', type=str, metavar='conn_name', help='Test database connection using a user-provided connection name')

    # parser.add_argument('-dbconfig', type=str, help='input name of the db config name matching from connections.yaml file')
   
    args = parser.parse_args()

    if args.dependencies:
        print("Project Dependencies:")
        for dep, version in DEPENDENCIES.items():
            print(f"{dep}: {version}")

    if args.example:
        print("Usage Information:\n")
        print(EXAMPLE)

    if args.connections:
        conn_manage_main()

    if args.yamldir:
        conn_home = os.getenv('conn_home')
        if conn_home:
            print(f"conn_home: {conn_home}")
        else:
            print("please set conn_home variable")

    if args.interactive:
        out =  interactive()
        print(out)
        sys.exit(0)

    if args.test:
        from .main_call import return_engine
        config_name = args.test
        try:
            engine = return_engine(config_name)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"✅ Connection '{config_name}' is working.")
        except Exception as e:
            print(f"❌ Connection '{config_name}' failed. Error:\n{e}")
        sys.exit(0)


if __name__ == '__main__':
    main()


