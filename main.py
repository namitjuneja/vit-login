from flask import Flask, request, jsonify
from test_parent import verify_student_data
import os, time


app = Flask(__name__)


@app.route('/home')
def hello_world():
	return "hey fucker"


@app.route('/', methods=["GET"])
def verify_student():
	reg_no = request.args.get("reg_no")
	dob = request.args.get("dob")
	mob_num = request.args.get("mob_num")

	data = verify_student_data(reg_no, dob, mob_num)
	return jsonify(**data)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
