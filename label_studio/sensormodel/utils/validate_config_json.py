import json
import jsonschema


def validateConfigJSON(config):
    schema = {
        "type": "object",
        "properties": {
            "date_row": {
                "type": "integer",
                "minimum": 1,
                "errors":{
                    "Date row must be an integer bigger than 0"
                }
            },
            "time_row": {
                "type": "integer",
                "minimum": 1,
                "errors":{
                    "Time row must be an integer bigger than 0"
                }
            },
            "timestamp_column": {
                "type": "integer",
                "minimum": 1,
                "errors":{
                    "Timestamp column must be an integer bigger than 0"
                }
            },
            "relative_absolute": {
                "type": "string",
                "enum": ["relative", "absolute"],
                "errors":{
                    "relative_absolute is either 'relative' or 'absolute'"
                }
            },
            "timestamp_unit": {
                "type": "string",
                "enum": ['days', 'hours', 'minutes', 'seconds', 'milliseconds', 'microseconds', 'nanoseconds'],
                "errors":{
                    "Timestamp unit must be one of the following options: 'days', 'hours', 'minutes', 'seconds', 'milliseconds', 'microseconds', 'nanoseconds'"
                }
            },
            "format_string": {
                "type": "string",
                "enum": ['DD/MM/YYYY','MM/DD/YYYY','YYYY/DD/MM','YYYY/MM/DD'],
                "errors":{
                    "Date format string must be one of the following options: 'DD/MM/YYYY','MM/DD/YYYY','YYYY/DD/MM','YYYY/MM/DD'"
                }
            },
            "sensor_id_row": {
                "type": "integer",
                "minimum": 1,
                "errors":{
                    "Sensor id row row must be an integer bigger than 0"
                }
            },
            "sensor_id_column": {
                "type": "integer",
                "minimum": 1,
                "errors":{
                    "Sensor id column must be an integer bigger than 0"
                }
            },
            "sensor_id_regex": {
                "type": "string"
            },
            "col_names_row": {
                "type": "integer",
                "minimum": 1,
                "errors":{
                    "Columns names row must be an integer bigger than 0"
                }
            },
            "comment_style": {
                "type": "string"
            },          
        },
        "required": ['date_row','time_row','timestamp_column','relative_absolute','timestamp_unit','format_string','sensor_id_row','col_names_row']
    }


    try:
        json_data = json.loads(config, parse_constant=True)
        jsonschema.validate(json_data, schema)
        print("The JSON data is valid according to the schema!")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print("The JSON data is not valid according to the schema:", e)
        
        print(e.message)
        return False

