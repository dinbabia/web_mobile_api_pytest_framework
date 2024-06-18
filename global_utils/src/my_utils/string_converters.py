def convert_string_to_bool(string):
    true_values = {"true", "1", "t", "yes", "y", "on"}
    false_values = {"false", "0", "f", "no", "n", "off"}

    string = string.strip().lower()

    if string in true_values:
        return True
    elif string in false_values:
        return False
    else:
        raise ValueError(f"Cannot convert '{string}' to boolean")
