from flask import Flask
from handlers.index import index_blue
from handlers.tools import tools_blue

app=Flask(__name__)
app.register_blueprint(index_blue)
app.register_blueprint(tools_blue)

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)
