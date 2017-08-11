echo "周日JOB数排序:"
cat flumedata |awk -F ":" '{print $2}'|sed '1!G;h;$!d'
