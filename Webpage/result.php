<?php 
require_once('connect.php'); 
$page = intval($_GET['page']);  //获取请求的页数 
$start = $page * 10; 
$result = $link->query("select Id, Author,Title,Text,Date,Time,LabelMood,Source from StockDataAL order by ID desc  limit $start,10"); 
while ($row=$result->fetch_array()) {
    $text = "sorry";
    $img_name = "niu.png";  
    if(strlen($row['Text']) > 200) {
        $text =utf8_substr($row['Text'],0,200); 
    } else {
        $text=$row['Text'];
    } 
    if($row['LabelMood']>0.5) {
        $img_name="up.png";
    } else {
        $img_name="down.png";
    }
    if($row['Source'] == "EAST") {
        $source="east.jpg";
    } 
    if($row['Source'] == "SINA") {
        $source="sina.jpg";
    } 
    $arr[] = array( 
        "id"=>$row['Id'],
        "author"=>$row['Author'], 
        "title"=>$row['Title'],
        "text"=>$text,
        "date"=>$row['Date'],
        "time"=>$row['Time'],
        "img_name"=>$img_name,
        "source"=>$source
    ); 
}
$link->close();
echo json_encode($arr);  //转换为json数据输出 
?>
