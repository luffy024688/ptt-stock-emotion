<?php
$db_host = 'localhost';
$db_name = 'ptt_stock';
$db_user = 'root';
$db_pass = '';

// data source name
$dsn = sprintf('mysql:host=%s;dbname=%s;charset=utf8', $db_host, $db_name);

$pdo_options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8",
];

try {
    $pdo = new PDO($dsn, $db_user, $db_pass, $pdo_options);
} catch (PDOException $ex) {
    echo 'Ex:' . $ex->getMessage();
}

$sql = "SELECT * FROM `article` WHERE `date` = '2019-11-30';
$rows = $pdo->query($sql)->fetchAll();

// CORS 問題
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

echo json_encode([
    'data' => $rows,
], JSON_UNESCAPED_UNICODE);
