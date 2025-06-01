<?php
// Cabeçalhos
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Tratar requisição OPTIONS (pré-flight CORS)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Lê dados JSON
$dados = json_decode(file_get_contents("php://input"), true);

// Validação simples
if (!$dados || !isset($dados['titulo'], $dados['autor'], $dados['genero'], $dados['preco'])) {
    http_response_code(400);
    echo json_encode(['erro' => 'Dados incompletos']);
    exit;
}

// Dados do formulário
$titulo = $dados['titulo'];
$autor = $dados['autor'];
$genero = $dados['genero'];
$preco = $dados['preco'];
$descricao = $dados['descricao'] ?? '';

// Conexão com o banco de dados (ajuste conforme seu ambiente)
$host = 'localhost';
$dbname = 'seubanco';
$user = 'root';
$pass = '';

// Conectar com PDO
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Inserir eBook
    $stmt = $pdo->prepare("INSERT INTO ebooks (titulo, autor, genero, preco, descricao) VALUES (?, ?, ?, ?, ?)");
    $stmt->execute([$titulo, $autor, $genero, $preco, $descricao]);

    echo json_encode(['mensagem' => 'eBook cadastrado com sucesso!']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['erro' => 'Erro ao conectar ou inserir no banco de dados: ' . $e->getMessage()]);
}
