from flask import Flask, request, render_template
from search import Search

app = Flask(__name__)
search = Search()


def perform_search(query):
    # 在这里完成具体的搜索操作，并返回一个结果列表
    search.receive_text(query)
    results = search.find_file()
    search.results = []
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('wd', '')  # 获取表单字段名为'wd'的值
        results = perform_search(query)  # 调用搜索函数进行搜索
        return render_template('results.html', query=query, results=results)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
