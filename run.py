from lecopain import app
import os
import sys

if __name__ == '__main__':
	app.secret_key = os.urandom(12)


	PARAM_DEBUG = sys.argv[1]
	PARAM_PATH_SECURITY = sys.argv[2]

	app.run(debug=True)


	#app.run(debug=PARAM_DEBUG, ssl_context=(PARAM_PATH_SECURITY+"/cert.pem", PARAM_PATH_SECURITY+"/key.pem"))