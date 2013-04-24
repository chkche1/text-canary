import nose
import requests
from nose.tools import eq_
import server

URL= 'http://localhost:5000/'

def get_json(url):
	return requests.get(URL+url).json()

# make sure that boston.txt and china.txt are both in uploads/
def test_emo_scale():
	results = eval(get_json('emotion_scale'))
	ans = {"results": [{
		  "./uploads/boston.txt": {
			"anger": 17, 
			"joy": 85, 
			"neutral": 7684, 
			"sadness": 34, 
			"fear": 17
		  }
		}, 
		{
		  "./uploads/china.txt": {
			"joy": 24, 
			"neutral": 1480, 
			"fear": 8
		  }
		}
	  ]
	}
	assert ans == results

def test_polarity_scale():
	results = eval(get_json('polarity_scale'))
	ans = {"results": [{"./uploads/boston.txt": {"positive": 391, 
		"negative": 578}}, 
		{"./uploads/china.txt": {"positive": 104, "negative": 152}
		}]}
	assert ans == results

def main():
	"""Our main function"""
	print "\n\nRunning unit tests...\n"
	if nose.run(argv=["--with-coverage", "test.py"]):
		print "\nPassed all unit tests"

if __name__ == "__main__":
	main()
