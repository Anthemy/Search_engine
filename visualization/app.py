from flask import Flask, render_template, request, jsonify
from markupsafe import Markup
from search import Search
# from flask_bootstrap import Bootstrap


# 创建一个flask应用
app = Flask(__name__)

@app.template_filter('highlight')
def highlight_words(text, words):
    for word in words:
        if word in text:
            text = text.replace(word, '<span class="highlight">{}</span>'.format(word))
    return Markup(text)


search = Search()

def perform_search(query):
    # 在这里完成具体的搜索操作，并返回一个结果列表
    search.receive_text(query)
    words = search.text
    results = search.sort_results()
    search.results = []
    return results, words



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('wd', '')  # 获取表单字段名为'wd'的值
        results, words = perform_search(query)  # 调用搜索函数进行搜索
        return render_template('results.html', query=query, results=results, words=words)
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
