import socket
import ssl
import re
import sys

from html.parser import HTMLParser

raw_list = []
data_list = []
tag_list = []
text_list = []
url_list = []
img_list = []
raw = ""
url = ""

if len(sys.argv) == 1:
    print("No arguments, i will use www.google.com for defaults\n")
    url = "www.google.com"
elif len(sys.argv) == 2:
    url = sys.argv[1]


def most_frequent_tag(L):
    count_dict = {}
    a = set(L)
    for i in L:
        if not (i in count_dict.keys()):
            count_dict[i] = 0
        else:
            count_dict[i] += 1
    list_d = list(count_dict.items())
    list_d.sort(key=lambda i: i[1])
    list_d.reverse()
    return list_d[0][0]


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        raw_list.append(tag)
        tag_list.append(tag)
        for attr in attrs:
            if attr[0] == "href":
                url_list.append(attr[1])

    def handle_data(self, data):
        raw_list.append(data)
        data_list.append(data)


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_default_certs()

port = 443
server_ip = socket.gethostbyname_ex(url)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = context.wrap_socket(sock, server_hostname=url)
sock.settimeout(1)
request = "GET / HTTP/1.1\r\nHost: " + url + "\r\n\r\n"

sock.connect((url, port))
sock.send(request.encode())

result = sock.recv(4096)

while len(result) > 0:
    try:
        result = sock.recv(4096)
        raw += result.decode()
    except socket.timeout:
        break
sock.close()

parser = MyHTMLParser()
parser.feed(raw)

img_regexp_tmp = re.findall(r"((http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png))", str(data_list))
for tmp in img_regexp_tmp:
    img_list.append(tmp[0])

for r in range(0, len(raw_list)):
    if raw_list[r - 1] in tag_list and not (raw_list[r - 1] == "script" or raw_list[r - 1] == "style"):
        if not raw_list[r] in tag_list:
            text_list.append(raw_list[r])
result = {}
result["List of tags"] = tag_list
result["Most frequent tag"] = most_frequent_tag(tag_list)
result["url list"] = url_list
result["text list"] = text_list
result["img list"] = img_list
print(result)
