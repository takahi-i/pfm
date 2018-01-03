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
    body.insert(0, headers)
    return body
