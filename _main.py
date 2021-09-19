from flask import *
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["TEMPLATE_DIR"] = "./templates"
# app.config["STATC_DIR"] = "./static"
app.config["DEBUG"] = True

@app.route('/')
def index():
    result = {"url": '', "imgs": [], "next": '', "prev": ''}
    return render_template('index.html', ctx=result)
    
@app.route('/search', methods=["POST", "GET"])
def search():
    url = request.args.get("curr_url")
    if "mangakakalot.tv" in url:
        result = _get_content_mangakakalot(request.args.get("curr_url"))
        return render_template('index.html', ctx=result)

    return render_template('index.html', ctx={"url": 'NOT FOUND', "imgs": [], "next": '', "prev": ''})
    

def _get_content_mangakakalot(url):
    # get page
    htmlpage = requests.get(url).content
    soup = BeautifulSoup(htmlpage, features="lxml")

    # find all <img>
    papers = soup.find_all("img")
    imgs = []
    for paper in papers:
        # print((paper))
        try:

            imgs.append(paper['data-src'])
        except:
            continue

    # find all next, prev btn
    buttons = {}
    btns = soup.find_all("a", {"class": "next"})
    for btn in btns:
        temp_txt = btn.text
        txt = ""
        for c in temp_txt:
            if c.isalpha():
                txt += c
        # print(txt)
        if txt == "PREVCHAPTER":
            buttons['prev'] = btn['href']
        else:
            buttons['next'] = btn['href']
    
    prev_url = f"https://ww.mangakakalot.tv{buttons['prev']}"
    next_url = f"https://ww.mangakakalot.tv{buttons['next']}"


    return {"url": url, "imgs": imgs, "next": next_url, "prev": prev_url}


def _get_content_nettruyen(url):
    # get page
    htmlpage = requests.get(url).content
    soup = BeautifulSoup(htmlpage, features="lxml")
    
    # find all <img>
    papers = soup.find_all("img")
    imgs = []
    for paper in papers:
        # print((paper))
        try:
            
            imgs.append(paper['src'])
        except:
            continue
    
    # find all next, prev btn
    buttons = {}
    btns = soup.find_all("a", {"class": "next"})
    for btn in btns:
        temp_txt = btn.text
        txt = ""
        for c in temp_txt:
            if c.isalpha():
                txt += c
        # print(txt)
        if txt == "PREVCHAPTER":
            buttons['prev'] = btn['href']
        else:
            buttons['next'] = btn['href']
    
    prev_url = f"https://ww.mangakakalot.tv{buttons['prev']}"
    next_url = f"https://ww.mangakakalot.tv{buttons['next']}"
    
    return {"url": url, "imgs": imgs, "next": next_url, "prev": prev_url}

if __name__ == '__main__':
    # app.secret_key = 'secret_key'
    app.run()