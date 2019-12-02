import os

path = '/var/www/html'
website = 'http://chyson.net'

black_list = ['index.html', '.git', 'show']
img_list = ['pics', 'pic', 'pictures', 'picture', 'show']

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
      a:hover {font-size:120%; text-decoration:none;}
      a:active {color: #0000ff;text-decoration:none;}
      
      .navigator div{float:left;
      margin:20px;
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
      <div><a href="http://chyson.net/show">Show</a></div>
      <div><a href="http://chyson.net/algorithm">Algorithm</a></div>
      <div><a href="http://chyson.net/ai">AI</a></div>
      <div><a href="http://chyson.net/books">Books</a></div>
    </div>
    <div style="clear:both;">
    <hr>
    </div>
'''

end = '''

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

    # print(inter_path)
    if inter_path.split(os.path.sep)[-1] in img_list:
        html += '<div class="show">\n'

        for ref in refs:

            # recursive generate index
            if os.path.isdir(join([base_path, inter_path, ref])):
                generate_index(base_path, join([inter_path, ref]))

            if ref in black_list:
                continue

            web_path = join([website, inter_path, ref])
            html += '<div>'
            html += '<img src="{}">'.format(web_path)
            html += '</div>\n'
        html += '</div>'
    else:
        html += '<div class="list">\n'
        html += '<ul>\n'

        for ref in refs:

            if os.path.isdir(join([base_path, inter_path, ref])):
                generate_index(base_path, join([inter_path, ref]))

            if ref in black_list:
                continue

            web_path = join([website, inter_path, ref])
            line = '<li>'
            line += '<a href="{}">{}</a>'.format(web_path, ref)
            line += '</li>'
            line += '\n'
            html += line

        html += '</ul>\n'
        html += '</div>'

    html += end

    with open(join([base_path, inter_path, 'index.html']), 'w') as f:
        f.write(html)


if __name__ == '__main__':
    generate_index(path)
