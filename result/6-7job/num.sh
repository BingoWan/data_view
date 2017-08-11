echo "周日入库数据量:"
cat flumedata |awk '{print $2}'|sed 's/日志增量://g'|sed 's/T,//g'|sed '1!G;h;$!d'
