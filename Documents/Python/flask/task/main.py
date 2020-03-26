from flask import Flask

import json
from utility_function import count_words,split_s
app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def hello():
    return "Hello! Internship.."

@app.route('/<str>/<n>',methods=['GET','POST'])
def split_string(str,n):
    return json.dumps(split_s(str,int(n)))


@app.route('/count/<str>',methods=['GET','POST'])
def count(str):
    return json.dumps(count_words(str))


if __name__ == '__main__':
    app.run(debug=True)