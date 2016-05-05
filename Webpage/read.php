<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">  
<html>  
<?php 
require_once('connect.php'); 
$Dir_Path = getcwd();
$Web_Name = substr($Dir_Path,strrpos($Dir_Path,'/')+1);
?>  
    <head>  
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
        <title>股票新闻推荐</title>  
        <style type="text/css">
        #container {
            padding-bottom: 29px;
            margin:10px auto;
            width:1000px;
            border-bottom: 1px solid #DCDCDC;
            overflow:hidden;
        }
        .vline {
            width:2px;
            height:500px;
            background:red;
            float:left;
            margin-top:60px;
            margin-left:20px;
        }
        .left {
            width:700px;
            float:left;
        }
        .right {
            width:250px;
            float:right;
            padding-left:20px;
        }
        .right .stockname p {
                width: 100%;
            text-align:left; 
            font-size:20px;
            color:red;
            }
        .right .trade_ralate {
            border:2px solid green;
            border-radius:10px;
            width:150px;
            color:green;
            margin-left:10px;
            margin-top:30px;    
            }
        .right .stock_ralate {
            border:2px solid green;
            border-radius:10px;
            width:150px;
            color:green;
            margin-left:10px;
            margin-top:30px;    
            }
        .right .positive p{
            width:150px;
            background:red;
            border-radius:5px;
            margin-left:10px;
            font:16px;
            color:white;
            text-align:center;
            }
        .right .negative p{
            width:150px;
            margin-left:10px;
            background:green;
            border-radius:5px;
            font:16px;
            color:white;
            text-align:center;
            }
        .right .keys p{
            width:150px;
            background:blue;
            border-radius:5px;
            margin-left:10px;
            font:16px;
            color:white;
            text-align:center;
            }
        .Title {
            width: 100%;
            margin-bottom: 16px;
            text-align:center;
            font-size:20px;
            color:#5188A6;
            line-height:30px;
        }
        .Text {
            width: 100%;
            height: auto;
            font-size:16px;
            float: left;
            margin-right: 20px;
            margin-left:2px;
            line-height:25px;
            text-align: justify ;
            display: block;
        }
        </style>  
        <script type="text/javascript" src = 
        <?php echo "/$Web_Name/static/js/jquery-2.0.3.min.js" ?>
        ></script>  
    </head>  
    <?php   
    if(isset($_GET['id'])) {
        $Id = $_GET['id'];
    } else {
    $Id = 1;
    }
        $result=$link->query("select Author,Title,Text,StockCode,StockName,LabelMood,LabelRelate,Positive,Negative,Trade from StockDataAL where id='$Id'");   
        $row=$result->fetch_array();
        $stock_name=$row['StockName'];
        $stock_code=$row['StockCode'];
        $stock_relate=$row['LabelRelate'];
        $trade_relate=$row['Trade'];
        $stock_relate =split(' ',$stock_relate);
        $trade_relate =split(' ',$trade_relate);
        $positives=split(' ',$row['Positive']);
        $negatives=split(' ',$row['Negative']);
        $text=$row['Text'];
        
    if($row['Positive'] != null) {
        foreach($positives as $p_value) {
            $text = preg_replace("/($p_value)/", '<span style="font-size:18px;color:white;border-radius:5px;background:red">\1</span>', $text);
        }
    }
    if ($row['Negative'] != null) {
        foreach($negatives as $n_value) {
            $text = preg_replace("/($n_value)/", '<span style="font-size:18px;color:white;border-radius:5px;background:green">\1</span>', $text);
        }
    }
    ?>  

    <div id="container">  
        <div class="left">
            <div class="Title"> 
                <?php 
                echo $row['Title'];
                echo "--";  
                echo $row['Author'];
                ?>
            </div> 
            <div class="Text"> 
                <p><?php echo $text;?> </p>
            </div>
        </div>
            <div class="vline"></div> 
            <div class="right">
                <h1 style="color:red;font-style: italic;">分析及建议</h1>
                <div class="stockname"><p> <?php echo $stock_name ,'-',$stock_code;?></p></div>
                <div class="keys">
                    <p>正向词VS负向词</p>
                </div>
                <div class="positive">
                    <p><?php echo $row['Positive']?></p>
                </div>
                <div class="negative">
                    <p><?php echo $row['Negative']?></p>
                </div>
                <div class="stock_ralate"> 
                    <h5 style="margin:15px;text-align:center;color:white;border:1 solid blue;background:blue;border-radius:5px;">关联股票--关联度</h5>
                    <?php 
                    for($i=0;$i<count($stock_relate);$i=$i+2){ 
                        if(round($stock_relate[$i+1],4)>"0.0000"){ ?>
                    <h5 style="margin:15px;text-align:center;"> <?php echo $stock_relate[$i],"-",round($stock_relate[$i+1],4);} ?></h5>
                <?php }?>
                </div>
                <div class="trade_ralate"> 
                    <h5 style="margin:15px;text-align:center;color:white;border:1 solid blue;background:blue;border-radius:5px;">关联行业--关联度</h5>
                    <?php 
                    for($i=0;$i<count($trade_relate);$i=$i+2){ 
                        if(round($trade_relate[$i+1],4)>"0.0000"){ ?>
                    <h5 style="margin:15px;text-align:center;"> <?php echo $trade_relate[$i],"-",round($trade_relate[$i+1],4);} ?></h5>
                <?php }?>
                </div>
                <h3 style="color:red;font-style: italic;">综合建议:<?php echo round($row['LabelMood'],6)?></h3>
            </div>
      </div>
</html>  
