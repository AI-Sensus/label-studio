import hashlib

def create_file_id(name, manufacturer, version, block_size=256):
    """
    Function that

    :param 
    :return: 
    """
    input_string = name + manufacturer + str(version)
    hashed = hashlib.sha256(input_string.encode()).hexdigest()
    return hashed[:10]



        