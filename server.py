from flask import Flask, session, redirect, url_for, escape, request
from flask import jsonify
from flask import render_template
from werkzeug import secure_filename
from scoop import futures
import nlp
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'data'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_page():
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
             <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        fi = request.files['file']
        if fi and allowed_file(fi.filename):
            filename = secure_filename(fi.filename)
            fi.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return upload_page()

    return upload_page()

@app.route('/remove/<filename>')
def remove_file(filename=None):
    if filename is None:
        return jsonify(error="Please specify the file to be removed")
    try:
        os.remove(UPLOAD_FOLDER+'/'+filename)
    except:
        return jsonify(error="Could not delete the file. Does it exist?")
    return jsonify(results="Successfully removed the file!")

@app.route("/tweet-pos", methods=['POST','GET'])
def twitter_pos():
    if request.method == 'POST':


        tweet = request.form['tweet']
        if len(tweet)!=0:
            ret = nlp.twit_pos(tweet)
            if ret is None:
                return jsonify(error="Can't tag your tweet!")
            return jsonify(results=ret)
    else:
        return render_template('tweet-pos.html')

@app.route('/spellcheck', methods=['POST','GET'])
def spellcheck():
    if request.method == 'POST':
        raw = request.form['raw']
        if len(raw) !=0:
            ret = nlp.spellcheck(raw)
            if ret is None:
                return jsonift(error="Can't do spellcheck!")
            return jsonify(results=ret)
    else:
        return render_template('spellcheck.html')

@app.route('/postag', methods=['POST','GET'])
def postag():
    if request.method == 'POST':
        raw = request.form['raw']
        if len(raw) !=0:
            ret = nlp.postag(raw)
            if ret is None:
                return jsonift(error="Can't do pos tagging!")
            return jsonify(results=ret)
    else:
        return render_template('postag.html')

@app.route('/emotion',methods=['POST','GET'])
def emotion():
    if request.method == 'POST':
        if 'option' not in request.form:
            return jsonify(error="must select an option for the NLP function!")
        raw, twit = request.form['raw'], False
        if request.form['option'] == 'twitter':
            twit=True
        if len(raw) !=0:
            ret = nlp.emotion_analysis(raw,twit)
            if ret is None:
                return jsonift(error="Can't do emotion analysis!")
            return jsonify(results=ret)
    else:
        return render_template('emotion.html')

@app.route('/polarity', methods=['POST','GET'])
def polarity():
    if request.method == 'POST':
        if 'option' not in request.form:
            return jsonify(error="must select an option for the NLP function!")
        raw, twit = request.form['raw'], False
        if request.form['option'] == 'twitter':
            twit=True
        if len(raw) !=0:
            ret = nlp.polarity_dist(raw, twit)
            if ret is None:
                return jsonift(error="Can't do analyze polarity distribution!")
            return jsonify(results=ret)
    else:
        return render_template('polarity.html')

@app.route('/pmi',methods=['POST','GET'])
def pmi():
    if request.method == 'POST':
        if 'option' not in request.form:
            return jsonify(error="must select an option for the NLP function!")
        raw, twit = request.form['raw'], False
        if request.form['option'] == 'twitter':
            twit=True
        if len(raw) !=0:
            ret = nlp.get_avg_pmi(raw, twit)
            if ret is None:
                return jsonift(error="Can't do analyze polarity distribution!")
            return jsonify(results=ret)
    else:
        return render_template('polarity.html')

@app.route('/spell_scale')
def spell_scale():
    return run_scale('spell_scale.py')

@app.route('/postag_scale')
def postag_scale(option=None):
    return run_scale('postag_scale.py')

@app.route('/emotion_scale')
def emotion_scale(option=None):
    return run_scale('emotion_scale.py')

@app.route('/polarity_scale')
def polarity_scale(option=None):
    return run_scale('polarity_scale.py')

def run_scale(script):
    try:
        output = subprocess.Popen(['python', '-m', 'scoop', script],\
                        stdout=subprocess.PIPE).communicate()[0]
        output = eval(str(output))
    except Exception as e:
        return jsonify(error=e)
    return jsonify(results=output)


if __name__ == '__main__':
    app.run(debug=True)
