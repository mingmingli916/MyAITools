import os_
import re

path = '/var/www/html'
website = 'https://chyson.net'

black_list = [r'index.html', r'.git', r'.aes', r'.gitignore', r'\W*.md', r'\W*.org', r'private$']
img_list = ['pics', 'pic', 'pictures', 'picture', 'fun']
video_suffix = ['.mp4', '.ogg', '.webm']
show_list = [
    'computer-systems-a-programmers-perspective',
    'deep-learning-for-computer-vision-with-python-imagenet',
    'deep-learning-for-computer-vision-with-python-practitioner',
    'deep-learning-for-computer-vision-with-python-starter',
    'introduction-to-algorithms',
    'latex-reference',
    # 'python-reference',
    'linux-bible',
    'deep-learning',
    # 'resources',
    # 'python3',
    'latex',
    'c',
    'learning-gnu-emacs',
    'mariadb',
    # 'pro-git',
    'what-life-should-meant-to-you'
]
show_list = sorted(show_list)

start = '''
<html style="color: rgba(255, 255, 255,0.8);">

  <head>
    <meta name="author" content="Mike Chyson">
    <meta charset="UTF-8">
    <meta name="description" content="Mike Chyson's Blog">
    <meta name="keywords" content="blog, python, ai, deep learning">
    <title>Chyson's Blog</title>

    <style type="text/css">
      a:link {text-decoration:none;}
      a:visited {color: rgba(255, 255, 255,0.8);text-decoration:none;}
      a:hover {background-color: rgb(250, 202, 46); text-decoration:none;border-radius:5px;color#000}
      a:active {color: rgba(255, 255, 255,0.8);text-decoration:none;}

      ul li{list-style-type:square}
      
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

  <body style="background:#000;margin:20px 40px">
    <div style="width:600px;margin:0 auto">
    <h1 style="color: rgb(250, 202, 46);">Mike Chyson's Blog</h1>
    <hr>
    <div class="navigator">
      <div><a href="https://chyson.net">Home</a></div>
      <div><a href="https://chyson.net/notes">Notes</a></div>
      <!-- <div><a href="https://chyson.net/notes/algorithm/leetcode">LeetCode</a></div> -->
      <!-- <div><a href="https://chyson.net/books">Books</a></div> -->
      <div><a href="https://chyson.net/papers">Papers</a></div>
      <div><a href="https://chyson.net/download">Download</a></div>
      <div><a href="https://chyson.net/fun">Fun</a></div>
      <!-- <div><a href="https://chyson.net/junjun">Junjun</a></div> -->

    </div>
    <div style="clear:both;">
    <hr>
    </div>
'''

end = '''

    <div id="info">
      <hr>
      <p>Name: Mingming Li (Mike Chyson)</p>
      <!--<p>Gender: Male</p>-->
      <p>Email: chyson@aliyun.com (mike.chyson@gmail.com)</p>
      <p>GitHub: <a class="github" href="https://github.com/mikechyson/">Mike Chyson</a></p>
      <!--<p>LeetCode: <a href="https://leetcode.com/user3394qq/"> Mike Chyson</a></p>-->
      <!--<p>Motto: THE BEST WAY TO LEARN SOMETHING IS TO USE IT!</p>-->
      <p>LinkedIn: https://www.linkedin.com/in/mike-chyson-2b743214a/</p>
      <p>School: Hebei University</p>
      <p>Facebook: https://www.facebook.com/profile.php?id=100043385618343</p>
    </div>

    <!--
    <div>
      <iframe src="https://chyson.net/notes/ai/deep-learning.html" width="100%" height="400" frameborder="1" scrolling="auto"></iframe>
    </div>
    -->
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
    return os_.path.sep.join(lst)


def generate_index(base_path, inter_path=''):
    html = start

    refs = os_.listdir(join([base_path, inter_path]))
    refs = sorted(refs, key=str.lower)

    if inter_path.split(os_.path.sep)[-1] in img_list:
        html += '<div class="show">\n'

        for ref in refs:

            # recursive generate index
            if os_.path.isdir(join([base_path, inter_path, ref])):
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

            if os_.path.isdir(join([base_path, inter_path, ref])):
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
    for show in show_list:
        for root, dirs, files in os_.walk(path):
            for file in files:
                if file.endswith('.html') and file.split('.')[0] == show:
                    line += '<li>'
                    line += '<a href="{}">{}</a>'.format(os_.path.join(root, file).replace(path, website),
                                                         file.split('.')[0].replace('-', ' ').replace('_', ' '))
                    line += '</li>\n'
    line += '</ul>\n'
    line += '</div>'
    return line


if __name__ == '__main__':
    generate_index(path)
