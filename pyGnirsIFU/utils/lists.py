def from_list_to_string(input_list):
    """

    Args:
        input_list:

    Returns:

    """
    if isinstance(input_list, list):
        if len(input_list) == 1:
            output_string = str(input_list[0])
        else:
            raise ValueError("Too many elements")
    elif isinstance(input_list, str):
        output_string = input_list
    else:
        raise TypeError("Only str or list implemented")
    return output_string