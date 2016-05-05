<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">  
<html xmlns="http://www.w3.org/1999/xhtml">  
<?php   
    require_once('connect.php');   
    $Dir_Path = getcwd();
    $Web_Name = substr($Dir_Path,strrpos($Dir_Path,'/')+1);
?>   
    <head>  
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
        <title>股票新闻推荐</title>  
    <!--<style type="text/css">@import url(/<?php echo $Web_Name;?>/static/css/index.css);</style> -->
    <link rel="stylesheet" type="text/css" href="<?php echo $Web_Name;?>/static/css/index.css" /> 
        <script type="text/javascript" src=
        <?php echo "/$Web_Name/static/js/jquery-2.0.3.min.js" ?>
        ></script>  
        <script type="text/javascript">  
            $(function() {  
        var winH = $(window).height(); //页面可视区域高度  
        var i = 1;
                $(window).scroll(function() {  
                    var pageH = $(document.body).height();  
                    var scrollT = $(window).scrollTop(); //滚动条top  
            var aa = (pageH - winH - scrollT) / winH;  
            if (aa < 0.02) { 
                        $.getJSON("/<?php echo $Web_Name;?>/result.php", {'page': i}, function(json) { 
            if (json) { 
                                $.each(json, function(index, array){ 
                        var str = "";
                    var str = "<div class=\"list\"><div class=\"picSource\"><img style=\"margin:25px 2px;\"src=\"/<?php echo $Web_Name;?>/";
                    var str = str + array["source"]+"\"></img></div>";
                    var str = str + "<div class=\"listTitle\"><h4 class=\"itemName\">"+ array["title"];
                    var str = str + "</h4>" +"<p class=\"author\"> "+array["date"]+"-"+array["time"]+"--"+array["author"];
                    var str = str + "</p></div><div class=\"picLeft\"> <img src=\"/<?php echo $Web_Name;?>/" +array["img_name"];
                    var str = str+ "\" style=\"margin-top:0px\" alt=\"<?php echo $Web_Name;?>\"> </div> <div class=\"listRight\"> " + array["text"]+"......";
                    var str = str +" <div class=\"listBottom\"> <a href=\"/<?php echo $Web_Name;?>/read.php?id=";
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
    <div class="section">
    <div class="lefWrap" id="container">
        <?php   
        $result=$link->query("select Id, Author,Title,Text,Date,Time,LabelMood,Source from StockDataAL order by ID desc limit 0,10");   
        while ($row=$result->fetch_array()) {   
        ?>   
    <div class="list">
        <div class="picSource">
        <?php if($row['Source'] == 'EAST') {?>
            <img style="margin:25px 2px; "src=
            <?php echo "/$Web_Name/east.jpg" ?>
            ></img>
            <?php } ?>
        
        <?php if($row['Source'] == 'SINA') {?>
            <img style="margin:25px 2px; "src=
            <?php echo "/$Web_Name/sina.jpg" ?>
            ></img>
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
                <img src=
                <?php echo "/$Web_Name/up.png" ?>
                style="margin-top:0px" alt=<?php echo $Web_Name;?>> 
            <?php
            } else {
            ?> 
                <img src=
                <?php echo "/$Web_Name/down.jpg" ?>
                style="margin-top:0px" alt=<?php echo $Web_Name;?>> 
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
            <a href='/<?php echo $Web_Name;?>/read.php?id=<?php echo $row['Id'];?>' >阅读全文</a>
            </div> 
        </div>
    <div class="clear"></div>       
      </div>
        <?php } ?>   
    </div> 
    </div>
    <div class="nodata">adf</div> 
