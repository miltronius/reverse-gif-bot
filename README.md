# reverse-gif-bot
Custom reverse gif bot for reddit.

Takes an reddit post that links to a gif on imgur, downloads it and reverts it. 

Technically, now, it's a python script that scrapes through reddit posts to find linked gifs, downloads the correlating mp4 file (Imgur converts gifs to gifv's which are mp4 files), and reverses it.

In a previous version it could upload gifs to Imgur, but the Imgur API would not allow files that are greater than 10MB. That's why I switched to getting mp4 files. But, the problem is now, that the Imgur API won't allow mp4 uploads either. Whew! Guess, I'll improve the script when I have a better solution.

# To Do (if you want to use it yourself)
- Create Reddit Account
- Add bot to Reddit
- Specify _praw.ini_
- Change authorization in _appconfig.py_

# General To Do
- Make it upload files to Imgur
- Take gifs from other linked pages
- Look through post comments and start action when someone wants to have a gif reversed
- Comment link for uploaded & reversed gif on reddit
- Additional commenting
- Make script able to run 24/7
