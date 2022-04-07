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


def _get_content_medoctruyen(url):
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
    
    if "medoctruyen" in url:
        result = _get_content_medoctruyen(request.args.get("curr_url"))
        return render_template('index.html', ctx=result)
    
    return render_template('index.html',
                           ctx={"url": "", "imgs": [], "next": '', "prev": ''})


@app.route('/cheat', methods=['GET', 'POST'])
def cheat():
    return render_template('wordzzle checker.html',
                           ctx={"not_in": "", "include_chars":"","knew_plot":"", "result": {}})

@app.route('/cheat/wordzzle', methods=['GET', 'POST'])
def wordzzle():
    not_in = request.args.get("not_in")
    included = request.args.get("in")
    knew_plot = request.args.get("knewpot")
    result = opt_filter(not_in, included, knew_plot)
    return render_template('wordzzle checker.html',
                           ctx={"not_in": not_in, "include_chars":included,"knew_plot":knew_plot, "result": result})


def not_contain(include_char, not_include_chars, word_mother, pos_list=[]):
    nincc = list(not_include_chars.lower())
    incc = list(include_char.lower())
    mwl = list(word_mother.lower())
    
    for c in nincc:
        if c in mwl:
            return False
    
    for c in incc:
        if c not in mwl:
            return False
    
    if pos_list == []:
        return True
    
    for pos_char_set in pos_list:
        if pos_char_set[0] > 0:
            if not mwl[pos_char_set[0] - 1].lower() == pos_char_set[1].lower():
                return False
        else:
            if mwl[pos_char_set[0] * -1 - 1].lower() == pos_char_set[1].lower():
                return False
    
    return True


def opt_filter(not_include_char, include_char, knew_pos):
    if not knew_pos == "":
        knew_position = knew_pos.split(" ")
        position_list = []
        for i in knew_position:
            if not i == "":
                if not "-" in i:
                    position_list.append((int(i[0]), i[1]))
                else:
                    position_list.append((int(i[1]) * -1, i[2]))
        # position_list = [(int(i[0]), i[1]) for i in knew_position if not i == ""]
        knew_pos = position_list
    else:
        knew_pos = []
    
    words = {}
    
    with open(r"\5-word-custom.txt", "r", encoding="utf-8") as r:
        lines = r.readlines()
        r.close()
    
    for line in lines:
        pair = line.replace("\n", "").split("\t")
        word = pair[0]
        meaning = pair[1]
        if word == "":
            break
        
        if not_contain(include_char, not_include_char, word, knew_pos):
            words[word] = meaning
    
    return words

if __name__ == '__main__':
    # app.secret_key = 'secret_key'
    app.run()
