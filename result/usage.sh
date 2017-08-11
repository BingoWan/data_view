#!/bin/bash
dir=/opt/zhoubao

##########HDFS_USAGE################
usage=`ls $dir/usage/*.csv`
echo '' > $dir/usage_result
for file in $usage
  do
    sum=`cat $file|wc -l`
    if [ $sum -lt 50 ];then
      val_hdfs=`cat $file |grep HDFS-5`
      #if [ ! -n "$val_hdfs" ];then
      if [ $sum -le 29 ] && [ ! -n $val_hdfs ];then
        cat $file|awk -F ',' '{print $1,$4/1024/1024/1024/1024}'|grep -v "entityName"|grep -v '^$'|awk '{num+=$2;if(FNR==4){print $1,num/FNR;FNR=0;num=0}} END{print $1,num/FNR}' >> $dir/usage_result
        echo "#####################################################################" >> $dir/usage_result
      else
        cat $file|awk -F ',' '{print $1,$3,$4}'|sed 's/nameservice1\|"//g'|grep -v "entityName"|grep -v '^$'|awk '{print $1,$2,$3/1024/1024/1024/1024}'|sed 's/T00:00:00.000Z//g' >> $dir/usage_result 
        echo "#####################################################################" >> $dir/usage_result
      fi
    else 
      cat $file|awk -F ',' '{print $1,$4/1024/1024/1024/1024}'|grep -v "entityName"|grep -v '^$'|awk '{num+=$3;if(FNR==24){print $1,num/FNR;FNR=0;num=0}} END{print $1,num/FNR}' >> $dir/usage_result
      echo "#####################################################################" >> $dir/usage_result
    fi
  done

#:<<BLOCK
##########DFS_USED##################
used=`ls $dir/used/*.csv`
echo '' > $dir/used_result
for file1 in $used
  do
    sum=`cat $file1|wc -l`
    if [ $sum -lt 80 ];then
      val=`cat $file1 |grep jydx`
      if [ ! -n "$val" ];then
        cat $file1|sed 's/"\|T00:00:00.000Z//g'|awk -F ',' '{printf "%s %s %s %.2f\n",$1,$2,$3,$4}'|grep -v "entityName"|grep -v '^$' >> $dir/used_result 
        echo "#####################################################################" >> $dir/used_result
      else
        #cat $file1|awk -F ',' '{printf "%s %s %s %.2f\n",$1,$2,$3,$4}'|grep jydx95 | awk '{num+=$5;if(FNR==4){print $1,num/FNR;FNR=0;num=0}} END{print $1,num/FNR}' >> $dir/used_result
        cat $file1|sed 's/"\|T00:00:00.000Z//g'|awk -F ',' '{printf "%s %s %s %.2f\n",$1,$2,$3,$4}'|grep -v "entityName"|grep -v '^$' >> $dir/used_result 
        echo "#####################################################################" >> $dir/used_result
      fi
    else
      cat $file1|awk -F ',' '{printf "%s %s %s %.2f\n",$1,$2,$3,$4}'|grep hzdx13|awk '{num+=$5;if(FNR==24){print $1,num/FNR;FNR=0;num=0}} END{print $1,num/FNR}' >> $dir/used_result
      echo "#####################################################################" >> $dir/used_result
    fi
  done

###########HBase_Region##############
region=`ls $dir/region/*.csv`
echo '' > $dir/region_result
for file2 in $region
  do
   # val_region=`cat $file2|grep HBase-G`
   # if [ ! -n "$val_region" ];then
    sum=`cat $file2|wc -l`
    if [ $sum -lt 29 ];then
      cat $file2|grep -v value|awk -F , '{printf "%d\n",$4}' >> $dir/region_result
      echo "#####################################################################" >> $dir/region_result
    else
      cat $file2|grep -v value|awk -F , '{printf "%d\n",$4}'|awk '{num+=$5;if(FNR==4){print $1,num/FNR;FNR=0;num=0}} END{print $1,num/FNR}' >> $dir/region_result
      echo "#####################################################################" >> $dir/region_result
    fi
  done
#BLOCK
