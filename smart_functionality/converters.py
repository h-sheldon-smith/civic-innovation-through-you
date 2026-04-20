'''
Method to convert data into AI friendly strings
Param: data, the data objects to be converted into AI friendly strings
Returns: data as string
'''
def Convert_Data(data):

    # There's no data
    if not data:
        return ""
    
    # The data doesn't need processing
    elif type(data) is str:
        return data
    
    # The data does need to be processed
    else:
        string = ""
        for field in data._meta.get_fields():
            value = getattr(data, field.name, None)
            value = str(value) if value is not None else ""

            string += f"{field.name}: {value}. "

        return string