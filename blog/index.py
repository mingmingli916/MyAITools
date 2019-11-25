import os

path = '/var/www/html'
website = 'http://chyson.net'

black_list = ['index.html', '.git', 'pics', 'show', 'pic']
white_list = ['html', 'pdf', 'hml']
show_path = os.path.join(path, 'show')

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
a:hover {font-size:150%; text-decoration:none; background:#66ff66;}
a:active {color: #0000ff;text-decoration:none;}
</style>
</head>

<body>

<h1 style="text-align:center">Mike Chyson's Blog</h1>


<hr>
'''

end = '''
<hr>
<div id="info">
  <p>Name: Mingming Li (Mike Chyson)</p>
  <p>Gender: Male</p>
  <p>Email: chyson@aliyun.com (mike.chyson@gmail.com)</p>
  <p>GitHub: <a class="github" href="https://github.com/mikechyson/">Mike Chyson</a></p>
  <p>Motto: THE BEST WAY TO LEARN SOMETHING IS TO USE IT!</p>
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
    refs = os.listdir(join([base_path, inter_path]))
    refs = sorted(refs, key=str.lower)

    html = start
    html += '<ul>'

    for ref in refs:
        if ref in black_list:
            continue

        if os.path.isdir(join([base_path, inter_path, ref])):
            generate_index(base_path, join([inter_path, ref]))

        web_path = join([website, inter_path, ref])

        line = '<li>'
        line += '<a href="{}">{}</a>'.format(web_path, ref)
        line += '</li>'
        line += '\n'
        html += line

        # elif ref.split('.')[-1] in white_list:
        #     web_path = join([website, inter_path, ref])
        #
        #     line = '<li>'
        #     line += '<a href="{}">{}</a>'.format(web_path, ref)
        #     line += '</li>'
        #     line += '\n'
        #     html += line
    html += '</ul>'
    html += '<hr>'
    show_html = generate_show()
    html += show_html

    html += end

    with open(join([base_path, inter_path, 'index.html']), 'w') as f:
        f.write(html)
    # print(html)


def generate_show():
    refs = os.listdir(show_path)
    refs = sorted(refs, key=str.lower)
    line = ''
    for ref in refs:
        line += '<div>'
        line += '<img src="/show/{}" width="400px">'.format(ref)
        line += '</div>'
    return line


if __name__ == '__main__':
    generate_index(path)
