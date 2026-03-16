from flask import Flask, render_template
from giangvien1.views import gv_bp

app = Flask(__name__)

app.register_blueprint(gv_bp)

if __name__ == '__main__':
       app.run(debug=True)

