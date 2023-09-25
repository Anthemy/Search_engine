import queue
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading  # 导入threading模块


class BFS:  # 广度优先遍历
    start_urls = ["https://baike.baidu.com"]
    count = 0
    queue = queue.Queue(maxsize=-1)  # 创建一个线程安全的队列对象
    visited = set()  # 创建一个集合对象，用于记录已访问过的链接

    def parse(self, response):
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=True)  # 提取当前页面的所有链接

        print(response.url)
        if response.headers.get("Content-Type", b"").startswith("text"):
            self.download(response)  # 下载当前页面

        for link in links:
            url = link['href']
            if url and not url.startswith('#') and not url.startswith('javascript:'):
                if url.startswith('http'):  # 判断链接是否是完整的网址
                    url = url
                else:  # 否则，将链接拼接成完整的网址
                    url = urljoin(response.url, url)

                url = url.replace("https", "http")  # 将https替换为http避免重复
                # print(url)
                try:
                    if url not in self.visited:  # 判断链接是否已经访问过
                        self.queue.put_nowait(url)  # 将链接加入队列
                        self.visited.add(url)  # 将链接加入集合
                except queue.Full:
                    print("Queue is full, skipping link")

        while not self.queue.empty():  # 循环遍历队列中的链接，直到队列为空
            try:
                next_url = self.queue.get_nowait()  # 取出队列中的第一个链接
                self.queue.task_done()  # 通知队列该链接已经完成
                next_response = requests.get(next_url)  # 发送请求，获取响应内容
                self.parse(next_response)  # 调用parse方法，继续提取链接和下载页面
            except queue.Empty:
                print("Queue is empty, no more links to crawl")
            except Exception as e:
                print(f'链接错误: {e}')
            finally:
                next_response.close()  # 关闭响应对象，释放资源

    def download(self, response):
        self.count += 1
        print(self.count)
        soup = BeautifulSoup(response.text, 'lxml')
        with open(f'./books/{self.count}.html', 'w', encoding='utf-8') as fp:
            title = None
            try:
                title = soup.find('title').text  # 提取网页标题
                description = soup.find('meta', attrs={'name': 'description'})['content']  # 提取网页描述
            except:
                description = None
            fp.write(f'id={self.count}\nurl={response.url}\ntitle={title}\ndescription={description}\ntext=')
            fp.write(response.text)


# 创建一个BFS对象，并调用其parse方法，开始爬虫
bfs = BFS()
response = requests.get(bfs.start_urls[0])  # 发送请求，获取响应内容
bfs.parse(response)
# threads = []  # 创建一个线程列表，用于存储和管理线程对象
#
# for i in range(10):  # 创建10个线程，并启动它们
#     t = threading.Thread(target=bfs.parse, args=(response,))  # 创建一个线程对象，指定目标函数和参数
#     t.start()  # 启动线程
#     threads.append(t)  # 将线程对象加入线程列表
#
# for t in threads:  # 等待所有线程完成任务
#     t.join()

print("Exiting Main Thread")
