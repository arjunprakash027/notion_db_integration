# DBIntegration Python Module

Read my [medium article](https://medium.com/@arjunprakash027/how-to-use-notion-database-to-power-your-software-and-storage-needs-611aad03e438) to know about how to create a notion database.

The `DBIntegration` module allows you to interact with Notion databases using Python. With this module, you can query, add, update, and delete entries in your Notion databases with ease.

## Installation

To use the `DBIntegration` module, you'll need to install the required `notion-db-integration` library. You can install it using pip:

```bash
pip install notion-db-integration==0.1.0
```

## Usage

First, import the module and create an instance of the `DBIntegration` class:

```python
from notion_db_integration import DBIntegration

# Initialize with your Notion integration token
ni = DBIntegration("your_integration_token")
```

### Get Available Databases

You can fetch a list of available databases linked to your integration key:

```python
databases = ni.get_databases()
print(databases)
```

### Set the Database

Before performing operations on a database, set the database you want to work with:

```python
ni.set_database("Database1")
```

### Get All Entries

You can retrieve all entries in the selected database:

```python
all_entries = ni.get_all_entries(dataframe=True)
print(all_entries)
```

### Query the Database

Query the database for entries that satisfy specific conditions. Here's how to query:

```python
# Single filter and single value to update
result = ni.query(query={"country":"india"}, dataframe=True)
print(result)

# Multiple filters and multiple values to update
result = ni.query(query={"country":"india","job":"engineer"}, dataframe=True)
print(result)
```

### Add a Single Value

You can add a single entry to the database:

```python
ni.add_value(value={"country":"india","job":"engineer","firstname":"shourav"})
```

### Add Multiple Values

To add multiple entries to the database:

```python
ni.add_values(values={
    "country":["india","usa"],
    "job":["engineer","doctor"],
    "firstname":["shourav","shubham"]
})
```

### Update Value

Update the value of one or more columns for specific records:

```python
# Single filter and single value to update
ni.update_value(filter_query={"country":"india"}, update_value={"job":"carpenter"})

# Multiple filters and multiple values to update
ni.update_value(filter_query={"country":"india","job":"engineer"}, update_value={"job":"carpenter","firstname":"babesh"})
```

### Delete Entry

Delete an entry by its ID:

```python
ni.delete_one(id=4)
```

## Troubleshooting

If you encounter any issues or errors while using this module, please make sure you have a valid integration token and that you're using it correctly.
Feel free to contact the module author for support and bug reports.
