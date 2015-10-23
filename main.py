from flask import Flask, request, jsonify
from test_parent import get_class_details_data, get_timetable_data, get_atten_data
import os, time


app = Flask(__name__)


@app.route('/home')
def hello_world():
	return "hey fucker"


@app.route('/class-details', methods=["GET"])
def login_class_details():
	reg_no = request.args.get("reg_no")
	dob = request.args.get("dob")
	mob_num = request.args.get("mob_num")

	data = get_class_details_data(reg_no, dob, mob_num)
	return jsonify(**data)


@app.route('/timetable', methods=["GET"])
def login_timetable():
	reg_no = request.args.get("reg_no")
	dob = request.args.get("dob")
	mob_num = request.args.get("mob_num")

	data = get_timetable_data(reg_no, dob, mob_num)
	return jsonify(**data)


@app.route('/attendance', methods=["GET"])
def login_atten():
	reg_no = request.args.get("reg_no")
	dob = request.args.get("dob")
	mob_num = request.args.get("mob_num")

	data = get_atten_data(reg_no, dob, mob_num)
	return jsonify(**data)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
