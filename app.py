from flask import Flask, request, jsonify, render_template, redirect
from src.drivers.url_shortner import generate_short_url
from src.repository.database import db
from src.models.url_sortned import UrlShortned
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_SECRET_KEY"] = "secret_key"
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        urls_data = UrlShortned.query.all()
        long_url = request.form["long_url"]

        check_long_url = [x.long_url for x in urls_data]       
        check_short_url = [x.short_url for x in urls_data]
        
        if long_url not in check_long_url:            
            short_url = generate_short_url()
            created_at = datetime.now()
            expire_at = created_at + timedelta(minutes=40)
            url_data = UrlShortned(long_url=long_url, short_url=short_url, created_at=created_at, expire_at = expire_at)
            db.session.add(url_data)
            db.session.commit()
        else:
            short_url = check_short_url[check_long_url.index(long_url)]        

        return jsonify({"short-url": f"{request.host_url}{short_url}"})
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_url(short_url):    
    url_data = UrlShortned.query.get(f"{short_url}")
    if url_data:
        return redirect(url_data.long_url)
    else:
        return jsonify({"message": "URL not found"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)