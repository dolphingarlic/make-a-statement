import base64
from urllib.request import urlopen 

from flask import Flask, make_response, request, render_template
from flaskext.markdown import Markdown
import pdfkit

app = Flask(__name__)
Markdown(app, extensions=['fenced_code'])


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/statement', methods=['POST'])
def statement():
    f = request.form
    name = f['name']
    shortname = f['shortname']
    contest = f['contest']
    order = f['order']
    language = f['language']
    logo_url = f['logo_url']
    accent_colour = f['accent_colour']
    description = f['description']
    inp = f['input']
    output = f['output']
    constraints = f['constraints']
    scoring = f['scoring']

    logo_b64 = base64.b64encode(urlopen(logo_url).read()).decode('utf-8')

    html = render_template('statement.html',
                           name=name,
                           shortname=shortname,
                           contest=contest,
                           order=order,
                           language=language,
                           logo=f'data:image/png;base64,{logo_b64}',
                           accent_colour=accent_colour,
                           description=description,
                           input=inp,
                           output=output,
                           constraints=constraints,
                           scoring=scoring
                          )
    
    options = {  
        'footer-center': 'Page [page] of [topage]',
        'quiet': '',
        'javascript-delay' : '5000',
        'page-size': 'A4',
    }
    pdf = pdfkit.from_string(html, False, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response
    # return html

if __name__ == '__main__':
    app.run()