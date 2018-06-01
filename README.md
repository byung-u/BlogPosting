# BlogPosting
Blog posting with python3


# nltk download failed
- https://github.com/keon/CodeGAN/issues/1

```
% python3
Python 3.6.5 (default, Mar 30 2018, 06:41:53)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import nltk
>>> nltk.download()
# and then type 'd' for download and install 'punkt'
```


# Memo
* powerful_twiterian.txt 파일에는 10만 이상의 팔로워가 있는 게정 정보가 있다.
  * `UNICEF 7080923 (UNICEF)` 이런 형식으로 저장되어있다.
* id와 nickname 정보를 조회하기위한 명령어  
  * `UNICEF (UNICEF)` 형태로 저리
  * `cat powerful_twiterian.txt | awk '{for(i=1;i<=NF;++i) if(i==2){continue;} else if(i==NF){printf("%s\n", $i);}else{printf("%s ", $i) }}'`
* 중복된 계정 횟수 순으로 오름차순 정렬해서 출력하기 
  * `5 UNICEF ` 형태로 저리
  * `cat powerful_twiterian.txt | sort -k 1 | awk '{print $1}' | uniq -c | sort -k 1 | awk '{if ($1!=1) print $1 " " $2}'`
