def merge_list_of_dict(list_of_dict: list) -> dict:
    """Merge a list of dict in a single dict, used for logging"""
    # TODO: refactor with dict.update ?
    merge_dict = {}
    for dictionary in list_of_dict:
        for k, v in dictionary.items():
            if k not in merge_dict:
                merge_dict[k] = [v]
            else:
                merge_dict[k].append(v)
    return merge_dict
