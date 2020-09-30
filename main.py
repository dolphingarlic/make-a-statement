import asyncio
import base64
from urllib.request import urlopen

from quart import Quart, make_response, request, render_template
from flaskext.markdown import Markdown
import pdfgen

loop = asyncio.get_event_loop()
app = Quart(__name__)
Markdown(app, extensions=['fenced_code'])


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/statement', methods=['POST'])
async def statement():
    f = await request.form
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

    if logo_url:
        logo_b64 = base64.b64encode(urlopen(logo_url).read()).decode("utf-8")
        logo_b64 = f'data:image/png;base64,{logo_b64}'
    else:
        logo_b64 = ''

    html = await render_template('statement.html',
                                 name=name,
                                 shortname=shortname,
                                 contest=contest,
                                 order=order,
                                 language=language,
                                 logo=logo_b64,
                                 accent_colour=accent_colour,
                                 description=description,
                                 input=inp,
                                 output=output,
                                 constraints=constraints,
                                 scoring=scoring
                                 )

    # return html
    pdf = await pdfgen.from_string(html)
    response = await make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

if __name__ == '__main__':
    app.run()
