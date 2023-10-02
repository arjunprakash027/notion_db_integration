import requests


class DBIntegration:

    def __init__(self, token):
        self.token = token
        self.headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2021-05-13',  # Replace with the latest API version
                }   

    def formatting(self,response,dataframe=False):
        from collections import defaultdict
        queried_database = defaultdict(list)
        try:
            data = response.json()
            entries = data.get('results', [])
            for entry in entries:
                for key,value in entry['properties'].items():
                    if key == "ID":
                        type = value['type']
                        queried_database[key].append(value[type]['number'])
                    else:
                        type = value['type']
                        queried_database[key].append(value[type][0]['plain_text'])
            if dataframe:
                import pandas
                return pandas.DataFrame(queried_database).reset_index(drop=True).set_index("ID")
            else:
                return dict(queried_database)
    
        except:
            raise Exception({"error":response.text})

    def get_databases(self) -> dict:
        """
        get all the databases linked with your integration key
        """
        self.avialable_databases = {}

        url = 'https://api.notion.com/v1/databases'
        response = requests.get(url, headers=self.headers)

        try:
            data = response.json()
            databases = data.get('results', [])
        
            
            for db in databases:

                self.avialable_databases[db['title'][0]['plain_text']] = db['id']
            
            return self.avialable_databases
                
        except:
            raise Exception ({"error":response.text})
    
    def set_database(self,db_name: str) -> str:
        """
        set the database to be used for the integration

        db_name = "name of the database"
        db_name is an required argument
        """

        if not db_name:
            raise Exception("db_name is required")
        
        self.columns_attributes = {}
        try:
            self.selected_database = self.avialable_databases[db_name]
            url = f"https://api.notion.com/v1/databases/{self.selected_database}"
            response = requests.get(url, headers=self.headers)

            for key,value in response.json()['properties'].items():
                 if key == "ID":
                     self.columns_attributes[key] = "number"
                 else:
                    self.columns_attributes[key] = value['type']
            
            return f"selected db {db_name} with id {self.selected_database}"
        except:
            raise Exception (f"db {db_name} not found")


    def get_all_entries(self,dataframe=False):
        """
        get all the entries in the selected database

        dataframe = True, returns a pandas dataframe
        """
        url = f'https://api.notion.com/v1/databases/{self.selected_database}/query'
        response = requests.post(url, headers=self.headers)

        return self.formatting(response,dataframe)
    
    def query(self,query,dataframe=False):
        """
        query the database for a particular entry or entries that satisfy some condition

        query:
        {"column":"value"}

        constraint: No multiple query allowed, will be introduced in future update
        """
    
        and_col = []

        url = f'https://api.notion.com/v1/databases/{self.selected_database}/query'

        for key,values in query.items():

            filter_conditions = {
                "property": key,
                self.columns_attributes[key]: {
                    "equals": values
                }
            }

            and_col.append(filter_conditions)
        
        filter_query = {
            "filter": {
                "and": and_col
            }
        }

        response = requests.post(url, headers=self.headers, json=filter_query)

        return self.formatting(response,dataframe)
    
    def add_value(self,value):
        
        """
        add a single value to database

        format:
        {"column1":value1,"column2":value2}


        """
        for key in value.keys():
            if key not in self.columns_attributes.keys():
                raise Exception(f"column {key} not found")
        
        url = f"https://api.notion.com/v1/pages"

        final_value = {}
        for key,content in value.items():
            final_value[key] = {self.columns_attributes[key]:[{'text':{'content':content}}]}
        
        new_entry_data = {
            'parent': {'database_id': self.selected_database},
            'properties': final_value
        }

        response = requests.post(url, headers=self.headers, json=new_entry_data)

        if response.status_code == 200:
            data = response.json()
            return f"New data added to the database {data['id']}"
        else:
            raise Exception(f"Failed to create a new page. Status code: {response.status_code}")
    
    def add_values(self,values):

        """
        Add multiple entries to the database

        values: {"country":["india","usa"],"job":["engineer","doctor"],"firstname":["shourav","shubham"]} -> example \n
        if there are no values for a particular entry use None instead of leaving it blank {"country":["india","usa"],"job":[None,"doctor"],"firstname":["shourav","shubham"]}
        """
        total_len = len(list(values.values())[0])

        new_entry_datas = []
        for key in values.keys():
            if len(values[key]) != total_len:
                raise Exception(f"column:{key} problem:length mismatch \n for empty value use None, do not leave it blank")
            if key not in self.columns_attributes.keys():
                raise Exception(f"column {key} not found")
        
        url = f"https://api.notion.com/v1/pages"

        for entries in range(total_len):
            final_value = {}
            for key,content in values.items():
                final_value[key] = {self.columns_attributes[key]:[{'text':{'content':content[entries]}}]}
            new_entry_data = {
            'parent': {'database_id': self.selected_database},
            'properties': final_value
            }
            new_entry_datas.append(new_entry_data)


        for entry_data in new_entry_datas:
            response = requests.post(url, headers=self.headers, json=entry_data)

            if response.status_code == 200:
                data = response.json()
                print(f"New entry created with ID: {data['id']}")
            else:
                raise Exception (f"Failed to create a new entry. Status code: {response.status_code}")
            
        return f"New entries added to the database"
    
    def update_value(self,filter_query,update_value):
        
        """
        update value of a given record(or records)

        useage:\n
        ->for single filter and single value to update:\n
        update_value(filter_query={"country":"india"},update_value={"job":"carpenter")

        ->for single filter and multiple values to update:\n
        update_value(filter_query={"country":"india"},update_value={"job":"carpenter","firstname":"babesh"})

        ->for multiple filter and single value to update:\n
        update_value(filter_query={"country":"india","job":"engineer"},update_value={"job":"carpenter"})

        ->for multiple filters and multiple values to update:\n
        update_value(filter_query={"country":"india","job":"engineer"},update_value={"job":"carpenter","firstname":"babesh"})
        """

        and_col = []
        properties_update = {}

        # column = list(filter_query.keys())[0]
        # value = list(filter_query.values())[0]

        column_update = list(update_value.keys())[0]
        value_update = list(update_value.values())[0]

        url = f'https://api.notion.com/v1/databases/{self.selected_database}/query'


        for key,values in filter_query.items():

            filter_conditions = {
                "property": key,
                self.columns_attributes[key]: {
                    "equals": values
                }
            }

            and_col.append(filter_conditions)
        
        filter_query = {
            "filter": {
                "and": and_col
            }
        }


        response = requests.post(url, headers=self.headers, json=filter_query)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results',[])

            for result in results:
                entry_id = result['id'] 
                update_url = f'https://api.notion.com/v1/pages/{entry_id}'

                for column_update,value_update in update_value.items():
                    
                    properties_update[column_update] = {
                                self.columns_attributes[column_update]: [
                                    {   
                                        "type":"text",
                                        "text":{"content": value_update}
                                    }
                                ]
                    }

                update_data = {
                    "properties": properties_update}

                update_response = requests.patch(update_url, headers=self.headers, json=update_data)

                if update_response.status_code == 200:
                    print("Entry updated successfully.")
                else:
                    raise Exception (f"Failed to update entry. Status code: {update_response.status_code}")

        else:
            raise Exception(f'Failed to fetch filtered database entries. Status code: {response.status_code}')


    def delete_one(self,id):
        
        """
        Delete an entry using ID.
        \n
        Useage:\n
        delete_one(id=id)\n

        will only accept id, do not pass anything\n
        """
        url = f'https://api.notion.com/v1/databases/{self.selected_database}/query'

        filter_conditions = {
        'property': 'ID',
        "number":{
            "equals":id
        }
    }

        filter_query = {
            "filter": {
                "and": [filter_conditions]
            }
        }

        response = requests.post(url, headers=self.headers, json=filter_query)

        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results',[])
            if len(results) == 1:
                # Retrieve the ID of the first entry
                entry_id = results[0]['id'] 
                update_url = f'https://api.notion.com/v1/pages/{entry_id}'

                update_data = {
                    "archived": True
                    }

                update_response = requests.patch(update_url, headers=self.headers, json=update_data)

                if update_response.status_code == 200:
                    print("Entry deleted successfully.")
                else:
                    raise Exception (f"Failed to delete entry. Status code: {update_response.status_code}")

        else:
            raise Exception ("Multiple entires found, cound not update")

if __name__ == "__main__":
    ni = DBIntegration("")
    ni.get_databases()
    ni.set_database("Database1")
    print(ni.get_all_entries(dataframe=True))
    # print(ni.query(query={"firstname":"New Name"},dataframe=False))
    #print(ni.add_value(value={"country":"india","job":"engineer","firstname":"shourav"}))
    #ni.add_values(values={"country":["india","usa"],"job":["engineer","doctor"],"firstname":["shourav","shubham"]})
    #ni.update_value(filter_query={"country":"india","job":"carpenter"},update_value={"job":"stockbroker","firstname":"amoly"})
    # ni.delete_one(id=4)