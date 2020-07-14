# freebuf_crawler

+ 用scrapy爬取freebuf文章信息，并生成可搜索(过滤器)的单页面
+ 袖珍但五脏俱全的freebuf文章搜索功能
+ 效果请参见 https://dog.wtf/freebuf

# 版本说明

由于freebuf于2020/07/01进行了改版更新，新版采用REST API即可获取文章基本信息，且原页面结构发生了变化，因此词此版本的程序已不可用，作为历史备份保存。

## 运行

进入`freebuf_crawler/`并执行

```bash
./run.sh
```

## 按
+ 😊 freebuf文章全面且历史沉淀丰富 
+ 😕 搜索功能不好用，可能是采用了全文检索的原因，需要权衡结果的相关性
+ 😕 按相关性和时间排序不能同时指定。按相关性排序时，结果是时间乱序的
+ 因此遇到例如如以下场景时。就难以得到想要的结果：
  + 只想按标题搜索某个应用所有漏洞和新闻，来系统性研究、学习
  + 想搜索"挖洞经验"，并按时间排序时

## 具体需求
+ 完善、高效、迅速的搜索功能
  + 标题
  + 日期
  + 文章等级
    + 红色标题
    + 金币奖励
    + 现金奖励
  + 标签
  + 浏览数
  + 评论数
  + 摘要
  + 以上所有AND组合搜索
+ 页面
  + 简洁的单页面
  + 暗色系
+ 数据爬取
  + 可中断与继续：参考[Jobs: pausing and resuming crawls](https://doc.scrapy.org/en/latest/topics/jobs.html)
  + 结果去重的增量爬虫，方便爬取新的文章：参考[keeping-persistent-state-between-batches](https://doc.scrapy.org/en/latest/topics/jobs.html#keeping-persistent-state-between-batches)

## 解决方案

### 环境
+ Python 3.7.5
+ scrapy 2.1.0
+ [tabulator](http://tabulator.info/)

### 思路
+ 依次爬取：https://www.freebuf.com/page/1 ~ https://www.freebuf.com/page/[N]
  + 页面没有文章，退出
  + 页面没有新文章，退出
+ 首次运行
  1. 爬取所有文章信息，写入json line文件`freebuf_crawler/freebuf.jl`
  2. 用`tabulator`实现方便查询(过滤)的单页面html模版
  3. 将爬取的结果数据注入单页面html模版，生成最终单页面html`freebuf_crawler/freebuf.html`
+ 非首次运行
  1. 爬取新的文章信息，加入到json line文件`freebuf_crawler/freebuf.jl`中
  2. 重新生成单页面html`freebuf_crawler/freebuf.html`

## 局限性
+ 由于下列原因
  + 靠page编号递增来爬取下一个页面
  + 根据页面是否有文章来判断退出
  + 目前18000+条文章
+ 导致
  + 爬取其实是单线程的
  + 首次爬取大概需要1个小时
  + 将目前18000+条新闻信息插入单页面中，导致页面大小略大，首次加载页面可能耗费些许时间
    + 未压缩html大小：5.4 MB
    + gzip压缩响应大小：2.1 MB
+ 由于是增量爬虫，第一次爬取完之后，后续运行只会爬取新的文章因此耗时很短


## 参考链接

+ [How to prevent duplicates on Scrapy fetching depending on an existing JSON list](https://stackoverflow.com/questions/51225781/how-to-prevent-duplicates-on-scrapy-fetching-depending-on-an-existing-json-list)
