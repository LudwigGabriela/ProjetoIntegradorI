<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Área do Administrador - ReadWise</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      display: flex;
    }

    /* Menu lateral */
    .sidebar {
      width: 200px;
      background-color: #6A8E3F;
      color: white;
      padding: 20px;
      height: 100vh;
    }

    .sidebar h2 {
      font-size: 18px;
      margin-bottom: 20px;
    }

    .sidebar a {
      display: block;
      color: white;
      margin-bottom: 10px;
      text-decoration: none;
      font-weight: bold;
    }

    .sidebar .sair {
      background-color: red;
      padding: 10px;
      color: white;
      border: none;
      text-align: center;
      display: block;
      margin-top: 30px;
      font-weight: bold;
    }

    .main {
      flex: 1;
      padding: 30px;
    }

    h1 {
      font-size: 24px;
      margin-bottom: 20px;
    }

    .form-section {
      background-color: #e0dcdc;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 30px;
    }

    .form-section input[type="text"],
    .form-section input[type="number"],
    .form-section textarea {
      width: 45%;
      padding: 10px;
      margin-bottom: 15px;
      border: none;
      border-radius: 5px;
    }

    .form-section button {
      background-color: #a1441b;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      font-weight: bold;
      cursor: pointer;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      background-color: white;
    }

    table th, table td {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: center;
    }

    .editar-btn, .excluir-btn {
      padding: 5px 10px;
      border: none;
      border-radius: 4px;
      font-weight: bold;
    }

    .editar-btn {
      background-color: #5a8ad2;
      color: white;
    }

    .excluir-btn {
      background-color: #d84c4c;
      color: white;
    }
  </style>
</head>
<body>

  <div class="sidebar">
    <h2>Área do Administrador</h2>
    <a href="#">Ebooks</a>
    <a href="#">Usuários</a>
    <a href="#">Assinaturas</a>
    <a href="#">Pedidos e Transações</a>
    <a href="#">Configurações</a>
    <a href="#">Promoções da Semana</a>
    <a href="#">Sugestões de Assinaturas</a>
    <button class="sair">Sair</button>
  </div>

  <div class="main">
    <h1><b>READ WISE</b></h1>

    <div class="form-section">
      <form id="formEbook">
        <input type="text" id="titulo" placeholder="Título do eBook" required>
    
        <select id="genero" required style="width: 45%; padding: 10px; margin-bottom: 15px; border: none; border-radius: 5px;">
            <option value="">Selecione um gênero</option>
            <option value="Romance">Romance</option>
            <option value="Fantasia">Fantasia</option>
            <option value="Suspense/Policial">Suspense/Policial</option>
            <option value="Acadêmico">Acadêmico</option>
        </select><br>
    
        <input type="text" id="autor" placeholder="Nome do Autor" required>
        <input type="number" id="preco" placeholder="Preço (R$)" required><br>
        
        <textarea id="descricao" rows="3" placeholder="Descrição" style="width: 92%; padding: 10px; margin-bottom: 15px; border: none; border-radius: 5px;"></textarea><br>
        
        <input type="file" id="arquivo"><br><br>
        
        <button type="submit">Cadastrar</button>
        </form>

    </div>
        <div id="tabelaEbooks" style="display: none; margin-top: 20px;">
            <h3>Lista de eBooks cadastrados</h3>
            <table border="1" width="100%" style="border-collapse: collapse;">
                <thead>
                <tr>
                    <th>Título</th>
                    <th>Autor</th>
                    <th>Gênero</th>
                    <th>Preço</th>
                    <th>Ações</th>
                </tr>
                </thead>
                <tbody id="corpoTabela">
                <!-- Linhas serão adicionadas com JavaScript -->
                </tbody>
            </table>
        </div>
            <button class="editar-btn">Editar</button>
            <button class="excluir-btn">Excluir</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>


<script>
 document.getElementById('formEbook').addEventListener('submit', async function(event) {
  event.preventDefault();

  const titulo = document.getElementById('titulo').value;
  const genero = document.getElementById('genero').value;
  const autor = document.getElementById('autor').value;
  const preco = document.getElementById('preco').value;
  const descricao = document.getElementById('descricao').value;
  const arquivo = document.getElementById('arquivo').files[0];

  const formData = new FormData();
  formData.append('titulo', titulo);
  formData.append('genero', genero);
  formData.append('autor', autor);
  formData.append('preco', preco);
  formData.append('descricao', descricao);
  formData.append('arquivo', arquivo);

  try {
    const response = await fetch('cadastrar_ebook.php', {
      method: 'POST',
      body: formData
    });

    const resultado = await response.text();
    alert(resultado);
    
    if (resultado.includes('sucesso')) {
      // Mostrar tabela
      document.getElementById('tabelaEbooks').style.display = 'block';

      // Adicionar nova linha na tabela
      const corpoTabela = document.getElementById('corpoTabela');
      const novaLinha = document.createElement('tr');
      novaLinha.innerHTML = `
        <td>${titulo}</td>
        <td>${autor}</td>
        <td>${genero}</td>
        <td>R$ ${parseFloat(preco).toFixed(2)}</td>
        <td>
          <button>Editar</button>
          <button>Excluir</button>
        </td>
      `;
      corpoTabela.appendChild(novaLinha);
    }

    // Limpar formulário
    document.getElementById('formEbook').reset();
  } catch (error) {
    alert('Erro ao cadastrar o eBook.');
    console.error(error);
  }
});


</script>

</body>
</html>


<?php
echo "Hello World";