from flask import Flask, render_template, redirect, request, send_from_directory
import os
import pyrebase
import random
import string

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyBV0KOB1ncUVgqRkQz5UfSocrs1V8AayN0",
  "authDomain": "url-shortener-32885.firebaseapp.com",
  "databaseURL": "https://url-shortener-32885.firebaseio.com",
  "projectId": "url-shortener-32885",
  "storageBucket": "url-shortener-32885.appspot.com",
  "messagingSenderId": "798839109196",
  "appId": "1:798839109196:web:c6e657c0081c288fb266e9",
  "measurementId": "G-RE7DF0N96K"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'link-icon.png', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        old = request.form["link"]
        connect = ""
        urls = []
        try:
            url_data = db.child("urls").get()
            for web_link in url_data.each():
                urls.append(web_link.val()[0])
        except:
            print(Exception)
        for i in range(0, 5):
            connect += random.choice(string.ascii_letters)
        new = "/" + connect
        while urls.count(new) > 0:
            connect = ""
            for i in range(0, 5):
                connect += random.choice(string.ascii_letters)
            new = "/" + connect
        print(urls)
        try:
            data = [new, old]
            db.child("urls").push(data)
            return redirect('/success' + new)
        except:
            return redirect('/failed')
    return render_template("main.html")

@app.route('/<link>')
def redirect_link(link):
    new_urls = []
    old_urls = []
    try:
        url_data = db.child("urls").get()
        for web_link in url_data.each():
            new_urls.append(web_link.val()[0])
            old_urls.append(web_link.val()[1])
    except:
        print(Exception)
    url = "/" + link
    if new_urls.count(url) == 0:
        return redirect('/failed')
    destination = old_urls[new_urls.index(url)]
    return redirect(destination)

@app.route('/success/<link>')
def success(link):
    new_urls = []
    old_urls = []
    try:
        url_data = db.child("urls").get()
        for web_link in url_data.each():
            new_urls.append(web_link.val()[0])
            old_urls.append(web_link.val()[1])
    except:
        print(Exception)
    url = "/" + link
    if new_urls.count(url) == 0:
        return redirect('/failed' + url)
    new_link = url
    old_link = old_urls[new_urls.index(new_link)]
    return render_template("success.html", new_link=new_link, old_link=old_link)

@app.route('/failed')
def failed():
    return render_template("failed.html")

@app.route('/unfound')
def unfound():
    return render_template("unfound.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('unfound.html'), 404

if __name__ == '__main__':
    app.run()

