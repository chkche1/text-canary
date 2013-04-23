from scoop import futures
import nlp
import glob

UPLOAD_PATH = './uploads/'
def spellcheck(filename):
	with open(filename, 'rU') as f:
		return {filename:nlp.spellcheck(f.read())}

if __name__ == "__main__":
	files = glob.glob(UPLOAD_PATH+'*.txt') + glob.glob(UPLOAD_PATH+'*.data')
	returnValues = list(futures.map(spellcheck, files))
	print returnValues
