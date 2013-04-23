from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
import nlp

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

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
		print 'form: ',request.form['option']
		if request.form['option'] == 'twitter':
			twit=True
		if len(raw) !=0:
			ret = nlp.get_avg_pmi(raw, twit)
			if ret is None:
				return jsonift(error="Can't do analyze polarity distribution!")
			return jsonify(results=ret)
	else:
		return render_template('polarity.html')


if __name__ == '__main__':
	app.run(debug=True)

