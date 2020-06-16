import json
from pprint import pformat

def format_data(f_data, encoding='urf-8'):
    formated_data = []
    BASE_URL = "https://www.freebuf.com/"
    for news_dict_str in f_data:
        news_dict = json.loads(news_dict_str.strip(), encoding=encoding)
        news = []
        news.append(news_dict.get('url').replace(BASE_URL, ''))
        news.append(news_dict.get('title'))
        news.append(news_dict.get('author'))
        news.append(news_dict.get('time'))
        news.append(news_dict.get('num_look'))
        news.append(news_dict.get('num_comment'))
        news.append(news_dict.get('level'))
        news.append('|'.join(news_dict.get('tags')))
        news.append(news_dict.get('text'))
        formated_data.append(news)
    # sort by time desc
    formated_data = sorted(formated_data, key=lambda x: x[3], reverse=True)
    return ',\n'.join(map(str, formated_data))

def generate_html(
        data_file='./freebuf.json',
        template_file='./template.html',
        template_str='{%data%}',
        output_html='./freebuf.html',
        encoding='utf-8'
    ):
    f_data = open(data_file, 'r', encoding=encoding)
    f_template = open(template_file, 'r', encoding=encoding)
    f_output = open(output_html, 'w', encoding=encoding)
    formated_data = format_data(f_data)
    f_output.write(f_template.read().replace(template_str, formated_data))
    f_data.close()
    f_template.close()
    f_output.close()


if __name__ == '__main__':
    generate_html(
        data_file='./freebuf.jl',
        template_file='./template.html'
    )