# BlogPosting
Blog posting with python3

# Memo
`cat powerful_twiterian.txt | awk '{for(i=1;i<=NF;++i) if(i==2){continue;} else if(i==NF){printf("%s\n", $i);}else{printf("%s ", $i) }}'`

