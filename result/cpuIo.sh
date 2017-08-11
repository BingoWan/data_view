#!/bin/bash

dir=/opt/zhoubao
#:<<BLOCK
####CPU-AVG#######
echo '' > $dir/cpu_tj
cpufiledir=`ls $dir/cpu`
for cpufile in $cpufiledir 
  do
    sum=`cat $dir/cpu/$cpufile|wc -l`
    if (( $sum == 29 ));then
      cat $dir/cpu/$cpufile|grep -v entityName|awk -F ',' '{print $1,$4}' >>$dir/cpu_tj
    else
      cat $dir/cpu/$cpufile|grep -v entityName|awk -F ',' '{print $1,$4}'|awk '{num+=$2;if(FNR==6){print $1,num/FNR;FNR=0;num=0}} END{print $1,num/FNR}' >>$dir/cpu_tj
    fi
  done
#BLOCK
#:<<BLOCK
####CLUSTER_IO_AVG######
echo '' > $dir/clusterio_tj
Ciofiledir=`ls $dir/clusterio/`
for Ciofile in $Ciofiledir 
  do
    sum=`cat $dir/clusterio/$Ciofile|wc -l`
    if (( $sum == 57 ));then
      cat $dir/clusterio/$Ciofile |grep -v entityName|awk -F ',' '{print $1,$2,$5}'|sed -e 's/\"\|stats(\|_bytes_rate_across_disks//g'|awk '{print $1,$2,$3/1024/1024}' >>$dir/clusterio_tj
    else
      cat $dir/clusterio/$Ciofile |grep -v entityName|awk -F ',' '{print $1,$2,$5}'|sed -e 's/\"\|stats(\|_bytes_rate_across_disks//g'|awk '{num+=$3;if(FNR==6) {print $1,$2,num/FNR;FNR=0;num=0}} END{print $1,$2,num/FNR}'|awk '{print $1,$2,$3/1024/1024}' >>$dir/clusterio_tj
    fi
  done
#BLOCK
