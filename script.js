document.getElementById('vaga-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const formData = new FormData(this);
    const empresaNome = formData.get('empresa_nome');
    const vagaTitulo = formData.get('vaga_titulo');
    // ... recuperar outros dados do formulário
  
    // Enviar dados para o Flask e o modelo Gemini
    fetch('/send_message', {
      method: 'POST',
      body: JSON.stringify({
        empresaNome: empresaNome,
        vagaTitulo: vagaTitulo,
        // ... enviar outros dados do formulário
      }),
    })
    .then(response => response.json())
    .then(responseData => {
      // Atualizar a tela com a resposta do chat
      const chatResponseElement = document.getElementById('chat-response');
      chatResponseElement.textContent = responseData.text;
    });
  });
  