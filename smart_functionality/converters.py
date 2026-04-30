'''
Method to convert data into AI friendly strings
Param: data, the data objects to be converted into AI friendly strings
Returns: data as string
'''
def Convert_Data(data):

    # Handles primitives
    if type(data) is str:
        return data
    
    elif isinstance(data, (bool, float, int)):
        return str(data)
    
    # Handles empty content
        # There's no data
    elif not data:
        return ""
    
    # The data does need to be processed
    elif hasattr(data, "_meta"):
        string = ""
        for field in data._meta.get_fields():

            if field.name not in ["id", "read_status", "file_location"]:
                value = getattr(data, field.name, None)

                if value:
                    value = str(value) if value is not None else ""
                    string += f"{field.name}: {value}. "

        return string
    
    else:
        return "Data conversion error has occured for type " + str(type(data))
    