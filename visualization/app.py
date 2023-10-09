from math import ceil
from flask import Flask, render_template, request
from markupsafe import Markup
from search import Search
from flask_paginate import Pagination

# 创建一个 flask 应用
app = Flask(__name__)

@app.template_filter('highlight')
def highlight_words(text, words):
    for word in words:
        if word in text:
            text = text.replace(word, '<span class="highlight">{}</span>'.format(word))
    return Markup(text)

search = Search()
results = []
words = []

def perform_search(query, page, per_page):
    # 在这里完成具体的搜索操作，并返回一个结果列表

    global results, words
    if not results:
        print('results:' ,results)
        search.receive_text(query)
        words = search.text
        results = search.sort_results()

    # 根据页码和每页结果数量进行分页
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_results = results[start_index:end_index]
    total_pages = ceil(len(results) / per_page)
    search.results = []
    return paginated_results, words, total_pages




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global results,words
        results = []
        query = request.form.get('wd', '')
        page = request.form.get('page', 1, type=int) # 修改这一行
        per_page = 20       # 每页的页数设置
        result, words, total_pages = perform_search(query, page, per_page)

        # 创建 Pagination 对象
        pagination = Pagination(page=page, per_page=per_page, total=len(result), record_name='results')

        return render_template('results.html', query=query, results=result, words=words, pagination=pagination, total_pages=total_pages,results_len=len(results))
    else:
        query = request.args.get('wd', '')
        print('query:' , query)
        if query:
            page = request.args.get('page', 1, type=int) # 修改这一行
            per_page = 20   # 每页的页数设置
            result, words, total_pages = perform_search(query, page,per_page)

            # 创建 Pagination 对象
            pagination = Pagination(page=page, per_page=per_page, total=len(result), record_name='results')

            return render_template('results.html', query=query, results=result, words=words, pagination=pagination, total_pages=total_pages,results_len=len(results))
        return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)