def convert_dictionary_to_2d_array(json_data):
    header = ["name", "type", "local_port", "remote_host", "host_port", "login_user", "ssh_server", "server_port"]
    body = []
    for name in json_data.keys():
        target = json_data[name]
        target_body = []
        for field in header:
            if field in target:
                target_body.append(target[field])
            else:
                target_body.append("")
        body.append(target_body)
    body.insert(0, header)
    return body
