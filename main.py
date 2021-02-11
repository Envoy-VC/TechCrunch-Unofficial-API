from flask import Flask
import bs4
import requests

app = Flask(__name__)

@app.route("/")
def articles():
    url = "https://techcrunch.com/"
    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    article_titles, article_contents, article_hrefs = [], [], []

    for tag in soup.findAll("div", {"class": "post-block post-block--image post-block--unread"}):
        tag_header = tag.find("a", {"class": "post-block__title__link"})
        tag_content = tag.find("div", {"class": "post-block__content"})

        article_title = tag_header.get_text().strip()
        article_href = tag_header["href"]
        article_content = tag_content.get_text().strip()

        article_titles.append(article_title)
        article_contents.append(article_content)
        article_hrefs.append(article_href)

    all_articles = []
    article_count = int(len(article_titles))

    for i in range(article_count):
        all_articles.append([])

    for i in range(article_count):
        all_articles[i].append(article_titles[i])
        all_articles[i].append(article_contents[i])
        all_articles[i].append(article_hrefs[i])

    data = {}
    data['articles'] = []
    for i in range(article_count):
        data['articles'].append({
            'title': article_titles[i],
            'content': article_contents[i],
            'url': article_hrefs[i]
        })

    return data

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)