import requests

import os
import requests

dump_directory = os.path.join(os.getcwd(), 'mp3')
os.makedirs(dump_directory, exist_ok=True)


def dump_mp4_for(resource):
    payload = {
        'api': 'advanced',
        'format': 'JSON',
        'video': resource
    }
    initial_request = requests.get('http://youtubeinmp3.com/fetch/', params=payload)
    if initial_request.status_code == 200:  # good to go
        download_mp4_at(initial_request)


def download_mp4_at(initial_request):
    j = initial_request.json()
    filename = '{0}.mp4'.format(j['title'])
    r = requests.get(j['link'], stream=True)
    with open(os.path.join(dump_directory, filename), 'wb') as f:
        print('Dumping "{0}"...'.format(filename))
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

response =requests.get("https://api.pexels.com/videos/search?query=fire&per_page=1&Authorization=563492ad6f91700001000001d45e41f296db4a08918d5f3c39016959")
example =response.json()
for i in range(10):
    print(example['videos'][0]['video_files'][i]['link'])