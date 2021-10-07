from bs4 import BeautifulSoup
from flask import *
from requests_html import *

app = Flask(__name__)
app.config["TEMPLATE_DIR"] = "./templates"
# app.config["STATC_DIR"] = "./static"
app.config["DEBUG"] = True


@app.route('/')
def index():
    result = {"url": '', "imgs": [], "next": '', "prev": ''}
    return render_template('index.html', ctx=result)


def _get_content_mangakakalot(url):
    htmlpage = requests.get(url).content
    soup = BeautifulSoup(htmlpage, features="lxml")
    
    papers = soup.find_all("img")
    imgs = []
    for paper in papers:
        try:
            
            imgs.append(paper['data-src'])
        except:
            continue
    
    buttons = {}
    buttons['prev'] = ""
    buttons['next'] = ""
    btns = soup.find_all("a", {"class": "next"})
    for btn in btns:
        temp_txt = btn.text
        txt = ""
        for c in temp_txt:
            if c.isalpha():
                txt += c
        if txt == "PREVCHAPTER":
            buttons['prev'] = btn['href']
        else:
            buttons['next'] = btn['href']
    
    next_url = ""
    prev_url = ""
    if not buttons['prev'] == "":
        prev_url = f"https://ww.mangakakalot.tv{buttons['prev']}"
    
    if not buttons['next'] == "":
        next_url = f"https://ww.mangakakalot.tv{buttons['next']}"
    
    return {"url": url, "imgs": imgs, "next": next_url, "prev": prev_url}


def _get_content_truyentranhlh(url):
    htmlpage = requests.get(url).content
    soup = BeautifulSoup(htmlpage, features="lxml")
    
    papers = soup.find_all("img")
    imgs = []
    for paper in papers:
        try:
            imgs.append(paper['data-src'])
        except:
            continue
    
    btns_prev = soup.find_all("a", {"class": "rd_sd-button_item2 rd_top-left"})
    btns_next = soup.find_all("a", {"class": "rd_sd-button_item2 rd_top-right"})
    
    buttons = {}
    buttons['prev'] = ""
    buttons['next'] = ""
    if len(btns_prev) > 0:
        buttons['prev'] = btns_prev[0]['href']
    if len(btns_next) > 0:
        buttons['next'] = btns_next[0]['href']
    
    next_url = buttons['next']
    prev_url = buttons['prev']
    
    return {"url": url, "imgs": imgs, "next": next_url, "prev": prev_url}


async def _get_content_nettruyen(url):
    session = AsyncHTMLSession()
    
    r = await session.get(url)
    await r.html.render()
    soup = BeautifulSoup(r.html.raw_html, features="lxml")
    
    papers = soup.find_all("img")
    imgs = []
    for paper in papers:
        try:
            if "gif" not in paper['src'] and "http" in paper['src']:
                imgs.append(paper['src'])
        except:
            continue
    
    btns_prev = soup.find_all("a", {"class": "prev"})
    btns_next = soup.find_all("a", {"class": "next"})
    
    buttons = {}
    buttons['prev'] = ""
    buttons['next'] = ""
    if len(btns_prev) > 2:
        buttons['prev'] = btns_prev[0]['href']
    if len(btns_next) > 2:
        buttons['next'] = btns_next[0]['href']
    
    next_url = buttons['next']
    prev_url = buttons['prev']
    
    return {"url": url, "imgs": imgs, "next": next_url, "prev": prev_url}


@app.route('/search', methods=["POST", "GET"])
def search():
    url = request.args.get("curr_url")
    if "mangakakalot" in url:
        result = _get_content_mangakakalot(request.args.get("curr_url"))
        return render_template('index.html', ctx=result)
    
    if "truyentranhlh" in url:
        result = _get_content_truyentranhlh(request.args.get("curr_url"))
        return render_template('index.html', ctx=result)
    
    return render_template('index.html',
                           ctx={"url": 'https://magasite.ext/manga/chap-05', "imgs": [], "next": '', "prev": ''})


if __name__ == '__main__':
    # app.secret_key = 'secret_key'
    app.run()
