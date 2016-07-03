# blog-img-download

네이버 블로그 포스팅 일부를 티스토리로 옮기는 중 이미지를 하나씩 다운 받는 것이 불편하여 제작하게 되었습니다. 네이버 블로그 html 문서의 구조가 변경될 경우 제대로 동작하지 않을 수 있습니다. 

## 개발환경

* 언어 : python 3.x
* IDE : Pycharm

## 사용방법

command line으로 블로그 게시물 주소를 인자로 전달하여 실행 합니다.
```
python blog_img_download.py 'http://blog.naver.com/yongho42/220095040554'
```

이미지 파일들은 해당 게시물의 제목과 동일한 디렉토리 하위에 생성됩니다.
