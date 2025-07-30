import json


def stream_response(response):
    for line in response.iter_lines():
        if not line:
            continue

        line_str = line.decode("utf-8")
        if not line_str.startswith("data: "):
            continue

        data_str = line_str[6:]  # Remove 'data: ' prefix

        if data_str == "[DONE]":
            break

        try:
            data_json = json.loads(data_str)
            yield data_json
        except json.JSONDecodeError:
            continue
