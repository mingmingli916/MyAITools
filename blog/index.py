import os
import re

path = '/var/www/html'
website = 'http://chyson.net'

black_list = [r'index.html', r'.git', r'.aes', r'.gitignore', r'\W*.md', r'\W*.org', r'private']
img_list = ['pics', 'pic', 'pictures', 'picture', 'fun']
video_suffix = ['.mp4', '.ogg', '.webm']
show_list = ['csapp',
             'deep-learning-for-computer-vision-with-python-imagenet',
             'deep-learning-for-computer-vision-with-python-practitioner',
             'deep-learning-for-computer-vision-with-python-starter',
             'introduction-to-algorithms',
             'reference',
             'linux-bible',
             'deep-learning',
             'resources',
             'python3',
             'latex',
             'c']

start = '''
<html>

  <head>
    <meta name="author" content="Mike Chyson">
    <meta charset="UTF-8">
    <meta name="description" content="Mike Chyson's Blog">
    <meta name="keywords" content="blog, python, ai, deep learning">
    <title>Chyson's Blog</title>

    <style type="text/css">
      a:link {text-decoration:none;}
      a:visited {color: #802A2A;text-decoration:none;}
      a:hover {background-color: #ddd; text-decoration:none;}
      a:active {color: #0000ff;text-decoration:none;}
      
      .navigator div{float: left;
      margin: 20px;
      }

      .show div{
      float:left;
      margin:10px;
      border: 3px solid black;
      }

      #info {
      clear: both
      }

    </style>

  </head>

  <body>

    <h1 style="text-align:center">Mike Chyson's Blog</h1>
    <hr>
    <div class="navigator">
      <div><a href="http://chyson.net">Home</a></div>
      <div><a href="http://chyson.net/notes">Notes</a></div>
      <!-- <div><a href="http://chyson.net/books">Books</a></div> -->
      <div><a href="http://chyson.net/papers">Papers</a></div>
      <div><a href="http://chyson.net/download">Download</a></div>
      <div><a href="http://chyson.net/fun">Fun</a></div>

    </div>
    <div style="clear:both;">
    <hr>
    </div>
'''

end = '''
    <iframe src="https://www.google.com/" width="100%" height="400" frameborder="1" scrolling="auto"></iframe>

    <div id="info">
      <hr>
      <p>Name: Mingming Li (Mike Chyson)</p>
      <p>Gender: Male</p>
      <p>Email: chyson@aliyun.com (mike.chyson@gmail.com)</p>
      <p>GitHub: <a class="github" href="https://github.com/mikechyson/">Mike Chyson</a></p>
      <!--<p>Motto: THE BEST WAY TO LEARN SOMETHING IS TO USE IT!</p>-->
    </div>

  </body>
</html>
'''


def join(lst):
    """
    Remove the effect of the empty string.
    This makes the a convenient way of joining path.
    :param lst:
    :return:
    """
    if '' in lst:
        lst.remove('')
    return os.path.sep.join(lst)


def generate_index(base_path, inter_path=''):
    html = start

    refs = os.listdir(join([base_path, inter_path]))
    refs = sorted(refs, key=str.lower)

    if inter_path.split(os.path.sep)[-1] in img_list:
        html += '<div class="show">\n'

        for ref in refs:

            # recursive generate index
            if os.path.isdir(join([base_path, inter_path, ref])):
                generate_index(base_path, join([inter_path, ref]))

            blocked = False
            for black in black_list:
                blocked = blocked or re.search(black, ref)

            if blocked or inter_path == '':
                continue

            web_path = join([website, inter_path, ref])
            html += '<div>'
            video_flag = False
            for suf in video_suffix:
                if ref.endswith(suf):
                    html += '<video width="320" height="240" controls="controls">'
                    html += '<source src="{}" type="video/mp4"/>'.format(web_path)
                    html += '<source src="{}" type="video/ogg"/>'.format(web_path)
                    html += '<source src="{}" type="video/webm"/>'.format(web_path)
                    html += '</video>'
                    video_flag = True
            if not video_flag:
                html += '<a href="{0}"><img src="{0}" width="400px"></a>'.format(web_path)
            html += '</div>\n'
        html += '</div>'
    else:
        html += '<div class="list">\n'
        html += '<ul>\n'

        for ref in refs:

            if os.path.isdir(join([base_path, inter_path, ref])):
                generate_index(base_path, join([inter_path, ref]))

            blocked = False
            for black in black_list:
                blocked = blocked or re.search(black, ref)

            if blocked or inter_path == '':
                continue

            web_path = join([website, inter_path, ref])
            line = '<li>'
            line += '<a href="{}">{}</a>'.format(web_path, ref)
            line += '</li>'
            line += '\n'
            html += line

        html += '</ul>\n'
        html += '</div>'

        if inter_path == '':  # top level
            show_html = generate_show()
            html += show_html

    html += end

    with open(join([base_path, inter_path, 'index.html']), 'w') as f:
        f.write(html)


def generate_show():
    line = ''
    line += '<div class="show">\n'
    line += '<ul>\n'
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.html'):
                for show in show_list:
                    if file.split('.')[0] == show:
                        line += '<li>'
                        line += '<a href="{}">{}</a>'.format(os.path.join(root, file).replace(path, website),
                                                             file.split('.')[0].replace('-', ' ').replace('_', ' '))
                        line += '</li>\n'
    line += '</ul>\n'
    line += '</div>'
    return line


if __name__ == '__main__':
    generate_index(path)
