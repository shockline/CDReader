<?php
$host="cp01-bdl-stock-001.epc.baidu.com";
$db_user="root";
$db_pass="213456";
$db_name="Stock_Data";
$db_port="5200";
$timezone="Asia/Shanghai";
$link=new mysqli($host,$db_user,$db_pass,$db_name,$db_port);
if ($link->connect_errno) {
    die('Connect Error: ' . $link->connect_errno);
}
$link->query("SET names UTF8");
function utf8_substr($str,$position,$length) {
    $start_position = strlen($str);
    $start_byte = 0;
    $end_position = strlen($str);
    $count = 0;
    for($i = 0; $i < strlen($str); $i++) {
        if($count >= $position && $start_position > $i) {
            $start_position = $i;
            $start_byte = $count;
        }
        if(($count-$start_byte)>=$length) {
            $end_position = $i;
            break;
        } 
        $value = ord($str[$i]);
        if($value > 127){
            $count++;
            if($value >= 192 && $value <= 223) $i++;
            elseif($value >= 224 && $value <= 239) $i = $i + 2;
            elseif($value >= 240 && $value <= 247) $i = $i + 3;
            else die('Not a UTF-8 compatible string');
        }
        $count++;
    }
    return(substr($str,$start_position,$end_position-$start_position));
}
?>
