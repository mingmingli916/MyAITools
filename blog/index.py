import os

path = '/var/www/html'
website = 'http://chyson.net'

black_list = ['index.html', '.git']
white_list = ['html', 'pdf', 'hml']

start = '''
<html>

<head>
<meta name="author" content="Hack Chyson">
<meta charset="UTF-8">
<meta name="description" content="Hack Chyson's Blog">
<meta name="keywords" content="blog, html, httpd">
<link rel="stylesheet" type="text/css" href="./css/index.css">
<title>Chyson's Blog</title>
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
    <p>GitHub: <a class="github" href="https://github.com/hackchyson/">hackchyson</a></p>
  </div>
  
</body>
</html>
'''


def join(lst):
    if '' in lst:
        lst.remove('')
    return os.path.sep.join(lst)


def generate_index(base_path, inter_path=''):
    refs = os.listdir(join([base_path, inter_path]))
    refs = sorted(refs)

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
    html += end

    with open(join([base_path, inter_path, 'index.html']), 'w') as f:
        f.write(html)
    # print(html)


if __name__ == '__main__':
    generate_index(path)
