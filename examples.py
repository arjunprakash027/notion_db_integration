from notion_db_integration import DBIntegration

ni = DBIntegration("")
print(ni.get_databases())
print(ni.set_database("Employment_db"))
print(ni.get_all_entries(dataframe=False))
# print(ni.query(query={"firstname":"New Name"},dataframe=False))
# print(ni.add_value(value={"country":"india","job":"engineer","firstname":"shourav"}))
#ni.add_values(values={"country":["india","usa"],"job":["engineer","doctor"],"firstname":["shourav","shubham"]})
#ni.update_value(filter_query={"country":"india","job":"stockbroker"},update_value={"job":"carpenter","firstname":"amoly"})
# ni.delete_one(id=4)