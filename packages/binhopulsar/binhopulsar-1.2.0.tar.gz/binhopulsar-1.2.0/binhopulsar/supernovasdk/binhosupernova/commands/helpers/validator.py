MIN_ID_VALUE = 1
MAX_ID_VALUE = 65535

def check_type(value, expected_type):
    """
    Checks if the value is of the expected type.

    Arguments
    ---------
    value
        Value to be checked.

    expected_type
        Expected type of the value.

    Returns
    -------
    bool
        True if the value is of the expected type, False otherwise.

    """
    return isinstance(value, expected_type)

def check_range(value, expected_type, min_val, max_val):
    """
    Checks if the value is within the valid range.

    Arguments
    ---------
    value
        Value to be checked.

    expected_type
        Expected type of the value.

    min_val
        Minimum value of the range.

    max_val
        Maximum value of the range.

    Returns
    -------
    bool
        True if the value is within the valid range, False otherwise.

    """
    return isinstance(value, expected_type) and min_val <= value <= max_val

def check_byte_array(data: list, max_size: int):
    """
    Checks if the data is a valid byte array.

    Arguments
    ---------
    data: list
        List of bytes to be checked.

    max_size: int
        Maximum size of the byte array.

    Returns
    -------
    bool
        True if the data is a valid byte array, False otherwise.

    """
    if( len(data) > max_size):
        return False
    return all(check_range(value, int, 0x00, 0xFF) for value in data)

def check_valid_id(id):
    """
    Checks if the id is within the valid range.

    Arguments
    ---------
    id: int
        ID to be checked.

    Returns
    -------
    bool
        True if the id is valid, False otherwise.

    """
    return check_range(id, int, MIN_ID_VALUE, MAX_ID_VALUE)

def getRepeatedItems(listOfItems: list):
    """
    Gets the repeated items from listOfItems

    Arguments
    ---------
    listOfItems: List to look into.

    Returns
    -------
    repeated
        List of the items from listOfItems that are repeated.

    """        
    seen = set()
    repeated = set()
    for value in listOfItems:
        if value in seen:
            repeated.add(value)
        else:
            seen.add(value)
    return (list(repeated))