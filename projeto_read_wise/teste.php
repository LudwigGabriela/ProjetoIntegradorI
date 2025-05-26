<?php

$host = "127.0.0.1:3306";
$usuario = "root";
$senha = "root";
$banco = "Read Wise";

$conn = new mysqli($host, $usuario, $senha, $banco);

if ($conn->connect_error) {
    die ("Erro de conexão: ".$conn->connect_error);
}

$titulo = $_POST['titulo'];
$genero = $_POST['genero'];
$autor = $_POST['autor'];
$preco = $_POST['preco'];
$descricao = $_POST['descricao'];

$nomeArquivo = "";
if (isset($_FILES['arquivo']) && $_FILES['arquivo']['error'] == 0) {
    $nomeArquivo = basename($_FILES["arquivo"]["name"]);
    $destino = "uploads/". $nomeArquivo;

    if (!is_dir("uploads")){
        mkdir("uploads", 0777, true);
    }

    move_uploaded_file($_FILES["arquivo"]["tmp_name"], $destino);
}

$sql = "INSERT INTO ebooks (titulo, genero, autor, preco, descricao, arquivo)
        VALUES(?, ?, ?, ?, ?, ?)";

$stmt = $conn->prepare($sql);
$stmt->bind_param("ssssss", $titulo, $genero, $autor, $preco, $descricao, $nomeArquivo);

if ($stmt->execute()) {
    echo "eBook cadastrado com sucesso!";
} else {
    echo "Erro ao cadastrar eBook: " . $conn->error;
}

$stmt->close();
$conn->close();


?>
