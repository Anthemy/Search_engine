from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

def read_reverse(input):  # 读取倒排表
    df = pd.read_csv("D:/PythonCode/搜索引擎_data/reverse_file/1.txt", header=None)
    df.columns = ['word', 'value']
    print(df.where(df['word'] == input).dropna()['value'].tolist())
    return df.where(df['word'] == input).dropna()['value'].tolist()

def perform_search(query):
    # 在这里完成具体的搜索操作，并返回一个结果列表
    results = read_reverse(query)
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
