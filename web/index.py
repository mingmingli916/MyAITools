import os

path = '/var/www/html'
website = 'http://chyson.net'

black_list = ['index.html']

start = '''
<html>

<head>
<meta name="author" content="Hack Chyson">
<meta charset="UTF-8">
<meta name="description" content="Hack Chyson's Blog">
<meta name="keywords" content="blog, html, httpd">
<link rel="stylesheet" type="text/css" href="./css/index.css">
<title>chyson's blog</title>
</head>

<body>

<h1 style="text-align:center"> Hack Chyson's Blog</h1>

<div id="motto">
  <p>The best way to learn something is to use it.</p>
</div>
<hr>
'''

end = '''
  <hr>

  <div id="github">
    <a class="github" href="https://github.com/hackchyson/">GitHub</a>
  </div>
  
</body>
</html>
'''


def list_files(path):
    result = []
    all = list_dirs(path)
    for a in all:
        if os.path.isfile(os.path.join(path, a)):
            result.append(a)
    return result


def list_dirs(path):
    result = []
    all = os.listdir(path)
    for a in all:
        if os.path.isdir(os.path.join(path, a)):
            result.append(a)
    return result


def generate_index(path, dir=None):
    all = os.listdir(path)

    html = start
    html += '<ul>'
    for a in all:
        if a in black_list:
            continue
        if dir is not None:
            rp = os.path.sep.join([website, dir, a])
        else:
            rp = os.path.sep.join([website, a])

        line = '<li>'
        line += '<a href="{}">{}</a>'.format(rp, a)
        line += '</li>'
        line += '\n'
        html += line
    html += '</ul>'
    html += end
    if dir is None:
        with open('index.html', 'w') as f:
            f.write(html)
    else:
        with open(os.path.join(dir, 'index.html'), 'w') as f:
            f.write(html)
    # print(html)

    dirs = list_dirs(path)
    for dir in dirs:
        generate_index(os.path.join(path, dir), dir=dir)


if __name__ == '__main__':
    # files = list_files(path)
    # for i in files:
    #     print(i)
    # dirs = list_dirs(path)
    # for i in dirs:
    #     print(i)
    generate_index(path)
