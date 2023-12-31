import requests
import json

HTTP_UNUSUAL_TRAFFIC = [403] # Forbidden

def get_remote(url, opts={}, verify_traffic_if_forbidden=True):
    response = requests.get(url, params=opts) 

    result = response.text
    headers = response.headers

    if verify_traffic_if_forbidden:
        for code in HTTP_UNUSUAL_TRAFFIC:
            if str(code) in headers and (code != 403 or verify_traffic_if_forbidden):
                print(f"HTTP code {code} detected. Please verify your traffic.")

    return result, headers

def get_json_string_from_html_script_prefix(html, script_prefix):
    html_part = html.split(f'>{script_prefix}', 2)[-1].split(';</script>', 2)[0]
    return html_part

def get_json_string_from_html(html, script_variable='', prefix='var '):
    if script_variable == '':
        script_variable = 'ytInitialData'

    script_prefix = f"{prefix}{script_variable} = "
    return get_json_string_from_html_script_prefix(html, script_prefix)

def does_path_exist(json_data, path):
    parts = path.split('/')
    parts_count = len(parts)

    if parts_count == 1:
        return parts[0] in json_data

    if parts[0] in json_data:
        return does_path_exist(json_data[parts[0]], '/'.join(parts[1:]))

    return False

def get_value(json_data, path):
    parts = path.split('/')
    parts_count = len(parts)

    if parts_count == 1:
        return json_data[path]

    return get_value(json_data[parts[0]], '/'.join(parts[1:]))

def get_most_replayed_data(video_id):
    result, _ = get_remote(f"https://www.youtube.com/watch?v={video_id}")
    html_content = result 

    json_str = get_json_string_from_html(html_content)
    json_data = json.loads(json_str) if json_str else None

    if json_data:
        # Perform operations with the obtained JSON data
        mutations = json_data['frameworkUpdates']['entityBatchUpdate']['mutations']
        common_json_path = 'payload/macroMarkersListEntity/markersList'
        json_path = f"{common_json_path}/markersDecoration"
        mutation = None

        for m in mutations:
            if does_path_exist(m, json_path):
                mutation = m
                break

        if mutation and does_path_exist(mutation, json_path):
            most_replayed = get_value(mutation, common_json_path)
            for marker in most_replayed['markers']:
                del marker['durationMillis']
                marker['startMillis'] = int(marker['startMillis'])

            timed_marker_decorations = most_replayed['markersDecoration']['timedMarkerDecorations']
            for decoration in timed_marker_decorations:
                for key in ['label', 'icon', 'decorationTimeMillis']:
                    del decoration[key]

            most_replayed['timedMarkerDecorations'] = timed_marker_decorations
            for key in ['markerType', 'markersMetadata', 'markersDecoration']:
                del most_replayed[key]
        else:
            most_replayed = None

        mostReplayed = {'mostReplayed': most_replayed}
        return mostReplayed
    else:
        print("No JSON data obtained.")
        return None
