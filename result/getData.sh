#!/bin/bash
dir=/opt/zhoubao
date1=`date -d "-8 day"  +%Y-%m-%d`
date2=`date -d "-1 day"  +%Y-%m-%d`
url_v1="T09%3A16%3A10.268Z&to="
url_v2="T09%3A16%3A10.268Z"
#:<<BLOCK
######GET CPU\IO DATA######
count=1
while read line
  do
    userpwd=`echo $line |awk '{print $1}'`
    ipaddr=`echo $line |awk '{print $2}'`
    if [ $ipaddr = "111.170.234.78" ];then
      curl -u "$userpwd" -o $dir/cpu/$count.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+cpu_percent_across_hosts+where+category+%3D+CLUSTER+and+clusterId+%3D+%221%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      curl -u "$userpwd" -o $dir/clusterio/$count.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+stats(read_bytes_rate_across_disks%2C+total)%2C+stats(write_bytes_rate_across_disks%2C+total)+where+category+%3D+CLUSTER+and+clusterId+%3D+%221%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      let count++;
      curl -u "$userpwd" -o $dir/cpu/$count.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+cpu_percent_across_hosts+where+category+%3D+CLUSTER+and+clusterId+%3D+%2214%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      curl -u "$userpwd" -o $dir/clusterio/$count.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+stats(read_bytes_rate_across_disks%2C+total)%2C+stats(write_bytes_rate_across_disks%2C+total)+where+category+%3D+CLUSTER+and+clusterId+%3D+%2214%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      let count++;
    else
      curl -u "$userpwd" -o $dir/cpu/$count.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+cpu_percent_across_hosts+where+category+%3D+CLUSTER+and+clusterId+%3D+%221%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      curl -u "$userpwd" -o $dir/clusterio/$count.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+stats(read_bytes_rate_across_disks%2C+total)%2C+stats(write_bytes_rate_across_disks%2C+total)+where+category+%3D+CLUSTER+and+clusterId+%3D+%221%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      let count++;
    fi
  done <$dir/aa
#BLOCK
###GET USAGE\USED DATA########
co=1
while read line
  do 
    userpwd=`echo $line |awk '{print $1}'`
    ipaddr=`echo $line |awk '{print $2}'`
    curl -u "$userpwd" -o $dir/usage/$ipaddr.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=%0A++++SELECT+dfs_capacity_used+WHERE+category%3DSERVICE+AND+serviceType%3DHDFS&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
    curl -u "$userpwd" -o $dir/used/$ipaddr.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+percent_used&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
    let co++;
  done < $dir/aa
#BLOCK

###GET REGION DATA#######
cou=1
while read line
  do
    userpwd=`echo $line |awk '{print $1}'`
    ipaddr=`echo $line |awk '{print $2}'`
    if [ $ipaddr = "111.170.234.78" ];then
      curl -u "$userpwd" -o $dir/region/$cou.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+total_regions_across_regionservers+where+entityName%3D%22hbase%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      let cou++
      curl -u "$userpwd" -o $dir/region/$cou.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+total_regions_across_regionservers+where+entityName%3D%22hbase5%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      let cou++
    elif [ $ipaddr = "113.107.58.95" ];then
      curl -u "$userpwd" -o $dir/region/$cou.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+total_regions_across_regionservers+where+entityName%3D%22hbase2%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
      let cou++
      curl -u "$userpwd" -o $dir/region/$cou.csv -D 1.header "http://$ipaddr:55000/api/v6/timeseries?query=select+total_regions_across_regionservers+where+entityName%3D%22hbase%22&contentType=text%2Fcsv&from=$date1$url_v1$date2$url_v2"
    fi
  done < $dir/aa
