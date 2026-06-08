document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatHistory = document.getElementById('chatHistory');
    const sendBtn = document.getElementById('sendBtn');

    // Manejar carga de archivos
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        uploadStatus.textContent = 'Subiendo y procesando...';
        uploadStatus.className = 'status-msg';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                uploadStatus.textContent = `✅ Listo. Indexados ${data.chunks} fragmentos.`;
                uploadStatus.className = 'status-msg';
            } else {
                throw new Error(data.detail || 'Error al subir');
            }
        } catch (error) {
            uploadStatus.textContent = `❌ Error: ${error.message}`;
            uploadStatus.className = 'status-msg error-msg';
        }
        
        // Resetear input para permitir subir el mismo archivo otra vez si se desea
        fileInput.value = '';
    });

    // Función para agregar mensajes al DOM
    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-msg' : 'bot-msg'}`;
        msgDiv.textContent = text;
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return msgDiv;
    }

    // Manejar envío de mensajes en el chat
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;

        // Mostrar mensaje del usuario
        addMessage(message, true);
        messageInput.value = '';
        
        // Bloquear input mientras responde
        messageInput.disabled = true;
        sendBtn.disabled = true;

        const loadingMsg = addMessage('Pensando...', false);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            if (response.ok) {
                loadingMsg.textContent = data.response;
            } else {
                throw new Error(data.detail || 'Error en el servidor');
            }
        } catch (error) {
            loadingMsg.textContent = `❌ Error: ${error.message}`;
            loadingMsg.classList.add('error-msg');
        } finally {
            messageInput.disabled = false;
            sendBtn.disabled = false;
            messageInput.focus();
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    });
});
