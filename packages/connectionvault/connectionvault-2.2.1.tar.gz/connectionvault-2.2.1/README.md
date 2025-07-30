[![Upload Python Package](https://github.com/ankit48365/ConnectionVault/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ankit48365/ConnectionVault/actions/workflows/python-publish.yml)
![Latest Release](https://img.shields.io/badge/release-v2.2.1-blue)
![CurrentLocal](https://img.shields.io/badge/machine-Latitude-brightgreen)

# ConnectionVault

```python
    pip install connectionvault
    connectionvault --help

```    
### Note

* version 2.0.0 Tested for postgres, sql server and mysql db
* version 2.1.1 Easier execution code, mysql db inetgrated, ReadMe updated with MCP inetgration
* version 2.2.0 Test connection from CLI {ex - connectionvault --test config_name}
* verson 2.2.1 OPtion 3 Display Conn hides Pass and present Tabular Data {ex - connectionvault --connections - [3] Display Connections

## Purpose

The purpose of this project is to centralize the database connections (credentials and other connections details) file (as YAML) on a user's machine.

## Running the Project : Pre-requisites

1. Create empty file ~ `connections.yaml` on a location of your choice.
2. Save that location as varibale path with name `conn_home`. 
3. Steps defined below as how to setup varibale on Windows and Linux

## For Windows (CMD):

```
# Define and save the path
setx conn_home "C:\path\outside\your\project\preferably"

# Check the path
echo %conn_home%

# Define and save the path
setx conn_home "C:\path\outside\your\project\preferably"

# Check the path
echo %conn_home%
```
## For Windows Powershell:

```
# Define and save the path
[System.Environment]::SetEnvironmentVariable('conn_home', 'C:\path\outside\your\project\preferably', 'User')

# Check the path
$env:conn_home
```

### For Linux:

```bash
# Define and save the path in your .bashrc
echo 'export conn_home="path/outside/your/project/preferably"' >> ~/.bashrc

# Source the .bashrc to apply changes
source ~/.bashrc
```

## Usage Examples:

From CLI run 

```
connectionvault --example
```

## MCP Integration:

On a MAchine where you have your Database running and want to spin MCP server, follow below steps:

1. Create project for MCP server
2. Install "connectionvault", "fastmcp"
3. Run a MCP server with a code like below

    ```
    from mcp.server.fastmcp.server import FastMCP 
    from src.main_call import return_string

    mcp = FastMCP("connections", log_level="ERROR")

    @mcp.prompt()
    def connections_prompt():
        return """
        You are interacting with a connections service that calls the 'connections' tool with a single parameter: req_string (string).
        this function when called returns a database connection string based on a match it finds on 'req_string' in a secure database credentials configuration file.
        """

    @mcp.resource("resource://empty")
    def empty_resource():
        return None  # Returns an empty resource


    @mcp.tool()
    def connections(req_string: str) -> str:
        db_config = return_string(req_string)  
        return db_config

    if __name__ == "__main__":
        mcp.run(transport='stdio')
    ```



### UML's

```
    pyreverse -o png -p myUML .
    or
    app\src> code2flow -o output.png cli.py connection_manager.py connection_utility.py
```
