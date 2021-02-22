from flask import Flask
from handlers.index import index_blue


app=Flask(__name__)
app.register_blueprint(index_blue)

if __name__=="__main__":
    app.run()
