# -*- coding: utf-8 -*-
import os
import urllib.request
import urllib
import sys


class ImgSrcParser:
    def __init__(self, url):
        self.src_url = url              # 원본 블로그 주소
        self.seq = 1                    # 저장될 이미지 이름(순서대로 번호 부여)
        self.userid, self.postid = self.get_userid_and_postid()     # 블로그 소유 유저의 id와 게시글 고유 번호 추출
        self.pure_document = self.get_pure_document()               # 전체 Html 문서 추출
        self.post_area = self.get_post_area()                       # 전체 Html 문서에서 블로그 본문만 추출
        self.title = self.get_title()

    def get_userid_and_postid(self):
        naver_blog_domain = "http://blog.naver.com/"  # 네이버 블로그 도메인
        return self.src_url[len(naver_blog_domain):].split("/")  # 0 : id, 1 : post id

    def get_pure_document(self):
        url = "http://blog.naver.com/PostView.nhn?blogId=" + self.userid + "&logNo=" + self.postid + \
              "&redirect=Dlog&widgetTypeCall=true"

        req = urllib.request.urlopen(url)
        charset = req.info().get_content_charset()
        return req.read().decode(charset)

    def get_post_area(self):
        start = "<div id=\"postViewArea\">"
        end = "<div class=\"post_footer_contents\">"

        start_pos = self.pure_document.find(start)
        end_pos = self.pure_document.find(end)

        return self.pure_document[start_pos:end_pos]

    def has_next(self):         # 블로그 본문을 탐색하며 이미지가 존재하는지 체크
        img_attr = "img src=\""
        start_pos = self.post_area.find(img_attr)
        if start_pos == -1:
            return False
        else:
            return True

    def next(self):             # 이미지 주소 추출
        img_attr = "img src=\""
        start_pos = self.post_area.find(img_attr)
        end_pos = self.post_area.find("\"", start_pos + len(img_attr))
        image_src = self.post_area[start_pos + len(img_attr):end_pos]
        self.post_area = self.post_area[end_pos:]
        return image_src

    def img_download(self, url):    # 해당 경로의 이미지 다운로드
        if "postfiles" not in url:
            print(url + " is not post image.")
            return

        self.make_directory()

        ext = url[url.rfind("."):url.rfind("?")]
        resource = urllib.request.urlopen(url)
        output = open(self.title + "/" + str(self.seq) + ext, "wb")
        output.write(resource.read())
        output.close()
        self.seq += 1
        print(url + " download success..")

    def get_title(self):
        start_tag = "<title>"
        end_tag = "</title>"
        start_pos = self.pure_document.find(start_tag) + len(start_tag)
        end_pos = self.pure_document.find(end_tag)

        return self.convert_space(self.remove_naver_caption(self.pure_document[start_pos:end_pos]))

    def remove_naver_caption(self, title):
        if "네이버 블로그" not in title:
            return title

        return title[:title.find(" : 네이버 블로그")]

    def convert_space(self, title):
        return title.replace(" ", "_")

    def make_directory(self):
        if not os.path.exists(self.title):
            os.makedirs(self.title)


if len(sys.argv) != 2:
    print("Please check your command.")
    print("ex) python blog_image_down.py 'http://blog.naver.com/example'")
else:
    parser = ImgSrcParser(sys.argv[1])
    while parser.has_next():
        parser.img_download(parser.next())
