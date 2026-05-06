import strip_markdown

'''
Method to convert data into AI friendly strings
Param: data, the data objects to be converted into AI friendly strings
Returns: data as string
'''
def Convert_Data(data):
  
    string = ""

    # Handles primitives
    if type(data) is str:
        string = data
    
    elif isinstance(data, (bool, float, int)):
        string = str(data)
    
    # Handles empty content
    # There's no data
    elif not data:
        return ""
    
    # The data does need to be processed (django table instance)
    elif hasattr(data, "_meta"):
        for field in data._meta.get_fields():
            if field.name not in ["id", "read_status", "file_location"]: # TODO: remove hardcoded logic
                value = getattr(data, field.name, None)

                if value:
                    value = str(value) if value is not None else ""
                    string += f"{field.name}: {value}. "
    
    else:
        return "Data conversion error has occured for type " + str(type(data)) #TODO: add tuple for failure: ,0


    # Remove markdown and return
    return strip_markdown.strip_markdown(string) #TODO: add tuple for success: ,1
