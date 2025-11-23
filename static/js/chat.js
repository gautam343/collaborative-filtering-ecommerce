const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const closeChat = document.getElementById('close-chat');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('chat-send');
const messagesContainer = document.getElementById('chat-messages');

// Toggle Window
chatToggle.addEventListener('click', () => {
    chatWindow.classList.toggle('active');
    if(chatWindow.classList.contains('active')) chatInput.focus();
});

closeChat.addEventListener('click', () => {
    chatWindow.classList.remove('active');
});

// Add Message to UI
function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Add Product Card to UI
function addProductCard(product) {
    const card = document.createElement('div');
    card.classList.add('chat-product-card');
    card.innerHTML = `
        <img src="/static/images/products/${product.image}" class="chat-product-img">
        <div class="chat-product-info">
            <h4>${product.name}</h4>
            <p>${product.category}</p>
        </div>
    `;
    // Make it clickable (optional - assume clicking shows details in real app)
    card.style.cursor = "pointer";
    messagesContainer.appendChild(card);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Send Message Logic
async function handleSend() {
    const text = chatInput.value.trim();
    if (!text) return;

    // 1. User Message
    addMessage(text, 'user');
    chatInput.value = '';

    // 2. Loading Indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'bot');
    loadingDiv.textContent = "...";
    loadingDiv.id = "chat-loading";
    messagesContainer.appendChild(loadingDiv);

    try {
        // 3. API Call
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        const data = await response.json();
        
        // Remove loading
        document.getElementById('chat-loading').remove();

        // 4. Bot Response
        addMessage(data.text, 'bot');

        // 5. Render Products if any
        if (data.products && data.products.length > 0) {
            data.products.forEach(prod => addProductCard(prod));
        }

    } catch (error) {
        document.getElementById('chat-loading').remove();
        addMessage("Sorry, I'm having trouble connecting. 😔", 'bot');
    }
}

sendBtn.addEventListener('click', handleSend);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});