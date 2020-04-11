def create_ordered_2d_array_from_dict(json_data, headers):
    rows = convert_dictionary_to_2d_array(json_data, headers)
    rows = sort_body_order(rows)
    rows = add_headers(rows, headers)
    return rows


def convert_dictionary_to_2d_array(json_data, headers):
    body = []
    for name in json_data.keys():
        target = json_data[name]
        target_body = []
        for field in headers:
            if field in target:
                target_body.append(target[field])
            else:
                target_body.append("")
        body.append(target_body)
    return body


def sort_body_order(body):
    body.sort(key=lambda x: x[0])
    return body


def add_headers(body, headers):
    body.insert(0, headers)
    return body
