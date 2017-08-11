#!/bin/bash
usage=`ls $dir/usage/*.csv`
echo '' > $dir/usage_result
for file in $usage
  do
    if [ "$file" = "111.170.234.78.csv" ];then
      cat $file|awk -F ',' '{print $1,$4/1024/1024/1024/1024}'|grep -v "entityName"|grep -v '^$'|awk '{num+=$2;if(FNR==4){print $1,num/FNR;FNR=0;num=0}} END{print $1,num/FNR}' >> $dir/usage_result
   
    fi
  done
