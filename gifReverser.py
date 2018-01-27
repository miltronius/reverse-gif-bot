#!/usr/bin/python
import praw
import re
import urllib3
import certifi
import imageio
from src import appconfig

imgurUrlPattern = re.compile(r'(https?://i.imgur.com/(.*))(\?.*)?')

def download_image(image_url, local_file_name):
    resp = http.request('GET', image_url, headers= {
        "Authorization": "Bearer " + appconfig.imgur['auth']
    }  ,preload_content=False)
    if resp.status == 200:
        print('Downloading %s...' % local_file_name)
        with open(local_file_name, 'wb') as fo:
            for chunk in resp.stream():
                fo.write(chunk)
    else:
        print('ERROR:', resp.status)
        for chunk in resp.stream():
            print(chunk)
    print('Download complete!')

# Create PoolManager instance
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
print(http)

# Create Reddit instance
reddit = praw.Reddit('reverse-gif-bot')

# Get the top values from our subreddit
subreddit = reddit.subreddit('gifs')
for submission in subreddit.hot(limit=5):
    # Check for all the cases where we will skip a submission:
    if "imgur.com/" not in submission.url:
        continue  # skip non-imgur submissions for now
    print('submission:',submission.title)
    localFileName = ''

    imgurFilename = submission.url.split('/').pop().split('.')[0] + '.mp4'
    newUrl = submission.url.split('m/')[0] + 'm/' + imgurFilename
    print('url:',newUrl,'imgurFilename:', imgurFilename)
    # download gif
    if '//i.imgur.com/' in submission.url:

        if '?' in imgurFilename:
            imgurFilename = imgurFilename[:imgurFilename.find('?')]
        localFileName = 'reddit_%s' % imgurFilename
        download_image(newUrl, localFileName)

    revFileName = localFileName.split('.')[0] + '_reversed.mp4'

    # REVERSE GIF & SAVE
    vid = imageio.get_reader(localFileName, 'ffmpeg')
    revVid = imageio.get_writer(revFileName, 'ffmpeg',fps=27,quality=7,macro_block_size=None)
    print('frames:',len(vid))
    percent = '|' # if (len(vid) - i) % 10 == 0: print(len(vid) - i,'/',len(vid))
    for i in range(len(vid)-1,0,-1):
        revVid.append_data(vid.get_data(i))

    vid.close()
    revVid.close()

    # UPLOAD GIF
    url = "https://api.imgur.com/3/upload.json"
    headers = {
        "Authorization": "Bearer " + appconfig.imgur['auth']
    }

    print('local file:', localFileName)
    print('reversed file:', revFileName)

    with open(revFileName, 'rb') as fp:
        uploadFile = fp.read()
    r = http.request(
        'POST',
        url,
        fields={
            'image': (revFileName, uploadFile),
            'name': imgurFilename + '_reversed',
            'title': imgurFilename + '_reversed'
        },
        headers=headers,
        preload_content = False
    )

    for chunk in r.stream(128):
        print(chunk)

#     add comment with link
#    submission.comments.replace_more(limit=0)
#    for comment in submission.comments.list():
#        print(comment.body)
