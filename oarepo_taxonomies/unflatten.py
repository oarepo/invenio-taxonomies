def unflatten(dictionary, sep="_"):
    result_dict = dict()
    for key, value in dictionary.items():
        parts = key.split(sep)
        d = result_dict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return result_dict


def convert_to_list(input):
    if isinstance(input, dict):
        list_ = []
        dict_ = {}
        islist = True
        i = 0
        keys = input.keys()
        isnumbers = all([k.isnumeric() for k in keys])
        if isnumbers:
            sorted_dict = sorted(input.items(),
                                 key=lambda item: int(item[0]) if item[0].isnumeric() else item[0])
        else:
            sorted_dict = sorted(input.items(),
                                 key=lambda item: str(item[0]))
        for k, v in sorted_dict:
            if k.isnumeric() and islist:
                if i == 0:
                    if not int(k) == 0:
                        islist = False
                        dict_[k] = convert_to_list(v)
                    else:
                        list_.append(convert_to_list(v))
                elif i > 0:
                    if str(i - 1) in input:
                        list_.append(convert_to_list(v))
                    else:
                        islist = False
                        dict_[k] = convert_to_list(v)

                else:
                    list_.append(convert_to_list(v))
            else:
                islist = False
                dict_[k] = convert_to_list(v)
            i += 1
        if islist:
            return list_
        else:
            return dict_

    if isinstance(input, (str, float, int)):
        return input


def unflatten_list(dictionary, sep="_"):
    return convert_to_list(unflatten(dictionary, sep=sep))
