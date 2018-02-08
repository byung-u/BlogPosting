# BlogPosting
Blog posting with python3

# Memo
* powerful_twiterian.txt 파일에는 10만 이상의 팔로워가 있는 게정 정보가 있다.
  * `UNICEF 7080923 (UNICEF)` 이런 형식으로 저장되어있다.
* id와 nickname 정보를 조회하기위한 명령어  
  * `UNICEF (UNICEF)` 형태로 저리
  * `cat powerful_twiterian.txt | awk '{for(i=1;i<=NF;++i) if(i==2){continue;} else if(i==NF){printf("%s\n", $i);}else{printf("%s ", $i) }}'`
* 중복된 계정 횟수 순으로 오름차순 정렬해서 출력하기 
  * `5 UNICEF ` 형태로 저리
  * `cat powerful_twiterian.txt | sort -k 1 | awk '{print $1}' | uniq -c | sort -k 1 | awk '{if ($1!=1) print $1 " " $2}'`
