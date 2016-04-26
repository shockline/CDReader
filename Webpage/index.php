<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">  
<html xmlns="http://www.w3.org/1999/xhtml">  
    <head>  
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
        <title>股票新闻推荐</title>  
        <style type="text/css"> 
            .section{
                margin:10px auto;
                width: 1050px;
                padding-bottom: 10px;
                }
            .leftWrap {
                width: 710px;
                }
            #container .list {
                width:650px;
                padding-bottom: 29px;
                margin-top: 24px;
                border: 1px solid gray ;
                border-radius:10px;
                margin-left:2px;
                margin-right:2px;
                overflow:hidden;
        
            }
            #container .list:hover {
                width:650px;
                padding-bottom: 29px;
                margin-top: 24px;
                border: 1px solid blue ;
                border-radius:10px;
                margin-left:2px;
                margin-right:2px;
                overflow:hidden;
            }
            .listTitle {
                width: 530px;
                text-align:center;
                float:right;
                overflow:hidden;
            }
                
            .listTitle .author {
                font:12px;
                color:#5188A6;
                text-align:right;
                padding-right:30px;
                margin-bottom: 10px;
            }
            .listTitle .itemName, .discovery_list .itemName, .signIn_title, .show_list .itemName {
                font-size: 20px;
                line-height: 30px;
                font-weight: normal;
                padding-left: 10px;
                color: #5188A6;
                margin-bottom:2px;
            }
            
            .picSource {
                width: 90px;
                height: 90px;
                float: left;
                margin-right: 20px;
                margin-left:2px;
                text-align: center;
                display: block;
                overflow: hidden;
            }
            .picLeft {
                width: 100px;
                height: 100px;
                float: left;
                margin-right: 20px;
                margin-left:2px;
                text-align: center;
                display: block;
                overflow: hidden;
            }
            .listRight {
                color: #666;
                width: 500px;       
                height: 80px;
                float: left;
            }
            .listBottom{
                float: right;
                z-index:2;
                height:30px;
                width:100%;
            }
            .listBottom a{
                margin-right: 0px;
                width: 79px;
                height: 30px;
                line-height: 30px;
                padding-left: 21px;
                font-size: 16px;
                float:right;
            }
            .clear {
                height: 0px;
                clear: both;
                overflow: hidden;
                font-size: 0px;
            }
            #container{margin:10px auto;width: 660px;overflow:hidden;}  
            .single_item{padding: 20px; border-bottom: 1px dotted #d3d3d3;}  
            .date{position: absolute; right: 0px; color:#999}  
            .content{line-height:20px; word-break: break-all;}  
            .element_head{width: 100%; position: relative; height: 20px;}  
            .nodata{display:none; height:32px; line-height:32px; text-align:center; color:#999; font-size:14px}  
        </style>  
        <script type="text/javascript" src="/stock-test/static/js/jquery-2.0.3.min.js"></script>  
        <script type="text/javascript">  
            $(function() {  
        var winH = $(window).height(); //页面可视区域高度  
        var i = 1;
                $(window).scroll(function() {  
                    var pageH = $(document.body).height();  
                    var scrollT = $(window).scrollTop(); //滚动条top  
            var aa = (pageH - winH - scrollT) / winH;  
            if (aa < 0.02) { 
                        $.getJSON("/stock-test/result.php", {'page': i}, function(json) { 
            if (json) { 
                                $.each(json, function(index, array){ 
                        var str = "";
                    var str = "<div class=\"list\"><div class=\"picSource\"><img style=\"margin:25px 2px;\"src=\"/stock-test/";
                    var str = str + array["source"]+"\"></img></div>";
                    var str = str + "<div class=\"listTitle\"><h4 class=\"itemName\">"+ array["title"];
                    var str = str + "</h4>" +"<p class=\"author\"> "+array["date"]+"-"+array["time"]+"--"+array["author"];
                    var str = str + "</p></div><div class=\"picLeft\"> <img src=\"/stock-test/" +array["img_name"];
                    var str = str+ "\" style=\"margin-top:0px\" alt=\"stock-test\"> </div> <div class=\"listRight\"> " + array["text"]+"......";
                    var str = str +" <div class=\"listBottom\"> <a href=\"/stock-test/read.php?id=";
                    var str = str + array['id'] ;
                    var str = str + "\">阅读全文</a></div></div><div class=\"clear\"></div></div>"; 
                                    $("#container").append(str);  
                                });  
                                i++;  
                            } else {  
                                $(".nodata").show().html("别滚动了，已经到底了。。。");  
                                return false;  
                            }  
                        });  
                    }  
                });  
            });  
        </script>  
    </head>  
    <?php   
    require_once('connect.php');   
    ?>   
    <div class="section">
    <div class="lefWrap" id="container">
        <?php   
        $result=$link->query("select Id, Author,Title,Text,Date,Time,LabelMood,Source from StockDataAL order by ID desc limit 0,10");   
        while ($row=$result->fetch_array()) {   
        ?>   
    <div class="list">
        <div class="picSource">
        <?php if($row['Source'] == 'EAST') {?>
            <img style="margin:25px 2px; "src="/stock-test/east.jpg"></img>
            <?php } ?>
        
        <?php if($row['Source'] == 'SINA') {?>
            <img style="margin:25px 2px; "src="/stock-test/sina.jpg"></img>
            <?php } ?>
        </div>
            <div class="listTitle"> 
            <h4 class="itemName">
            <?php 
            echo $row['Title'];
            ?>
            </h4>
            <p class="author">
            <?php
            echo $row['Date'],'-',$row['Time'],"--";
            echo $row['Author'];
            ?>
            </p>
            </div> 
        <div class="picLeft">   
            <?php
            if($row['LabelMood']>0.5){
            ?>
                <img src="/stock-test/up.png" style="margin-top:0px" alt="stock-test"> 
            <?php
            } else {
            ?> 
                <img src="/stock-test/down.png" style="margin-top:0px" alt="stock-test"> 
            <?php
            }
            ?>
            </div> 
        <div class="listRight">   
            <?php 
            $text = ""; 
            if(strlen($row['Text']) > 200) {
                    $text = utf8_substr($row['Text'],0,200);
            } else { 
                    $text= $row['Text'];
                    }
            echo $text;
            echo "......";
            ?> 
            <div class="listBottom"> 
            <a href='/stock-test/read.php?id=<?php echo $row['Id'];?>' >阅读全文</a>
            </div> 
        </div>
    <div class="clear"></div>       
      </div>
        <?php } ?>   
    </div> 
    </div>
    <div class="nodata">adf</div> 
