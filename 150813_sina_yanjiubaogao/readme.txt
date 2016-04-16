vip.stock.finance.sina.com.cn

[MainUrl格式]
http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/search/index.phtml?symbol=股票代码&t1=all

[Label](以'\t'分割)
stockname	stockcode	url	标题	报告类型	发布日期	机构	研究员	正文

[File]
nohup python catch005.py 1>stock.txt 2>errlog.txt &
1>stdout : stock.txt
2>stderr : errlog.txt