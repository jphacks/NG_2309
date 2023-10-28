from flask import *
from pathlib import Path

base_dir = Path(__file__).parents[1]
static_dir = base_dir / "frontend" / "static"


app = Flask(__name__,
            static_folder=static_dir)


@app.route("/")
def index():
    return render_template("html/index.html")


if __name__ == "__main__":
    app.run(debug=True)