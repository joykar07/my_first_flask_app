from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Gourab'

if __name__ == "__main__":
    app.run(debug=True)


print("Hello World")
print("test2")