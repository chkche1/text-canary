from scoop import futures
import nlp
import glob
import sys

UPLOAD_PATH = './uploads/'
def analyze_emotion(filename):
	with open(filename, 'rU') as f:
		return {filename:dict(nlp.emotion_analysis(f.read()))}

if __name__ == "__main__":
	files = glob.glob(UPLOAD_PATH+'*.txt') + glob.glob(UPLOAD_PATH+'*.data')
	ret = futures.map(analyze_emotion, files)
	print([x for x in ret if isinstance(x,dict)])

