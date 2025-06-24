document.addEventListener("DOMContentLoaded", function() {
    const image = document.querySelector("img");

    if (image) {
        image.addEventListener("click", function() {
            document.body.style.backgroundColor = getRandomColor();

            showAnimatedagina/MouraMessage("Você clicou na imagem!");
        });
    }

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    function showAnimatedMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('animated-message');
        messageDiv.innerText = message;
        document.body.appendChild(messageDiv);

        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 2000);
    }
});

// WebSocket:

const socket = io('http://localhost:8080');

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('form');
    const loginButton = document.getElementById('setUsers');

    if (loginForm && loginButton) {
        loginButton.addEventListener('click', (event) => {
            const usernameInput = document.getElementById('username').value;

            if (usernameInput) {
                // Envia o username via WebSocket
                socket.emit('login', { username: usernameInput });
                alert('Login anunciado');
            }
            loginForm.submit();
        });
    } else {
        console.error('Form or login button not found');
    }
});
