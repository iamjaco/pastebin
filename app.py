from flask import Flask, render_template, request, redirect, url_for, abort
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

pastebin = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        pastebin.append(content)
        return redirect(url_for('paste', index=len(pastebin)-1))
    return render_template('index.html')

@app.route('/paste/<int:index>')
def paste(index):
    try:
        content = pastebin[index]
    except IndexError:
        abort(404)  # Return a 404 error if the requested index does not exist
    return render_template('paste.html', content=content, index=index)

if __name__ == '__main__':
    app.run(debug=True)