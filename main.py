from flask import Flask, render_template
from assess import assess_bp
from list_sb import list_sb_bp

app = Flask(__name__)

# Đăng ký Blueprint
app.register_blueprint(list_sb_bp)
app.register_blueprint(assess_bp)

def home():
    @app.route('/')
    def index():
        return render_template("base.html")
    return app
if __name__ == '__main__':
    app = home()
    app.run(debug=True)
