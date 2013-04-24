from scoop import futures
import nlp
import glob

UPLOAD_PATH = './uploads/'
def tagFile(filename):
    with open(filename, 'rU') as f:
        return {filename: nlp.postag(f.read())}

if __name__ == "__main__":
    files = glob.glob(UPLOAD_PATH+'*.txt') + glob.glob(UPLOAD_PATH+'*.data')
    returnValues = list(futures.map(tagFile, files))
    print returnValues
