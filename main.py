from flask import Flask, request, redirect, render_template
import datetime, os
from getChat import *
from replit import db
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )


@app.route('/')
def index():
    with open("template/Main.html", "r") as f:
        page = f.read()
    with open("template/Components/header.html", "r") as f:
        header = f.read()
    with open("template/Components/footer.html", "r") as f:
        footer = f.read()
    page = page.replace("{header}", header)
    page = page.replace("{footer}", footer)

    return page


@app.route('/DrawZone')
def DrawZone():
    with open("template/Draw/DrawZone.html", "r") as f:
        page = f.read()
    with open("template/Components/header.html", "r") as f:
        header = f.read()
    with open("template/Components/footer.html", "r") as f:
        footer = f.read()
    page = page.replace("{header}", header)
    page = page.replace("{footer}", footer)

    return page


@app.route('/Therpist')
def TherapistChat():

    with open("template/therapist/chat.html", "r") as f:
        page = f.read()

    with open("template/Components/header.html", "r") as f:
        header = f.read()

    with open("template/Components/footer.html", "r") as f:
        footer = f.read()

    page = page.replace("{chats}", getChat())

    page = page.replace("{header}", header)
    page = page.replace("{footer}", footer)

    return page


@app.route('/add', methods=["POST"])
def add():
    form = request.form
    urmessage = form["message"]
    date = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(date)
    prompt = (
        f"You are a therpist and your patient said this {urmessage}, be as short as possible. Answer in the same language the user is using. Your answer must be under 50 words"
    )
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="llama3-8b-8192",
    )

    Airesponse = response.choices[0].message.content
    db[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = {
        "urmessage": request.form['message'],
        "Airesponse": Airesponse
    }

    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
