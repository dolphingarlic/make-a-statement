import time

from quart import Quart, make_response, request, render_template
from flaskext.markdown import Markdown
import pyppeteer

app = Quart(__name__)
Markdown(app, extensions=['fenced_code'])
pyppeteer_opts = {
    'format': 'A4',
    'printBackground': True,
    'margin': {'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'},
}


@app.route('/')
async def home():
    return await render_template('index.html')


async def create_pdf(html):
    browser = await pyppeteer.launch(options={'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.setContent(html)
    time.sleep(3)
    pdf = await page.pdf(pyppeteer_opts)
    await browser.close()
    return pdf


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

    html = await render_template('statement.html',
                                 name=name,
                                 shortname=shortname,
                                 contest=contest,
                                 order=order,
                                 language=language,
                                 logo_url=logo_url,
                                 accent_colour=accent_colour,
                                 description=description,
                                 input=inp,
                                 output=output,
                                 constraints=constraints,
                                 scoring=scoring
                                 )

    pdf = await create_pdf(html)
    response = await make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

if __name__ == '__main__':
    app.run()
