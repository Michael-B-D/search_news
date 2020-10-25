import requests
import json
from flask import Flask, render_template, request
import os


KEY = os.environ['API_KEY']
url = "https://rapidapi.p.rapidapi.com/v1/search"

headers = {
    'x-rapidapi-host': "newscatcher.p.rapidapi.com",
    'x-rapidapi-key': KEY
    }
    
app = Flask(__name__, static_folder="templates", static_url_path="")

@app.route('/')
def get_results():
    free_text = request.args.get('free_search')
    if not free_text:
        free_text = request.args.get('optional_free_text')
        if not free_text:
            return render_template('index.html')
    country = request.args.get('country_search')
    time_from = request.args.get('time_form_search')
    time_to = request.args.get('time_to_search')
    sort_by = request.args.get('sortby_search')
    page = request.args.get('page')
    filter_results = {}
    all_articles = []
    if not page:
        page = 1
    else:
        page = str(page)
    querystring = {"q":free_text, "media":"True", "country":country, "from":time_from, "to":time_to, "page":page}
    print('query',querystring)
    response = requests.request("GET", url, headers=headers, params=querystring)
    print('COntent:',response.text)
    res = json.loads(response.text)
    if res['status'] == 'ok':
        print('WORK', response.status_code, response.text)
        filter_keys = ['total_hits', 'page', 'total_pages']
        filter_results = {key: value for key, value in res.items() if key in filter_keys}
        filter_results['page'] = int(filter_results['page'])
        filter_keys_article = ['title', 'link', 'media', 'clean_url', 'published_date']
        for article in res['articles']:
            try:     
                if article['media'] == None:
                    article['media'] = 'images/newspaper-regular.svg'
            except KeyError as e:
                print(e)
                article['media'] = 'images/newspaper-regular.svg'
                all_articles.append({key: value for key, value in article.items() if key in filter_keys_article})
                continue
            all_articles.append({key: value for key, value in article.items() if key in filter_keys_article})
        return render_template(
            'results_page.html',
            filter_results=filter_results,
            all_articles=all_articles,
            status=res['status'],
            current_url=request.url,
        )
    else:
        print('dont work', response.status_code)
        return render_template(
            'main_page_no_mach.html',
            status=res['status']
            )

            
app.run(debug=True)
