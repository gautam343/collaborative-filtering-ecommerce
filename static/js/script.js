// ... (Keep the mobile menu & accordion code exactly as it was) ...

/* ============================================
   ENHANCED RECOMMENDATION ENGINE LOGIC
============================================ */

const recModal = document.getElementById('rec-modal');
const recClose = document.getElementById('rec-close');
const recGrid = document.getElementById('rec-grid');
const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');

const summaryImg = document.getElementById('summary-img');
const summaryName = document.getElementById('summary-name');
const summaryPrice = document.getElementById('summary-price');

const closeModal = () => {
    recModal.classList.remove('active');
};
recClose.addEventListener('click', closeModal);
recModal.addEventListener('click', (e) => {
    if(e.target === recModal) closeModal();
});

const modalActionBtns = document.querySelectorAll('.btn-modal');
modalActionBtns.forEach(btn => btn.addEventListener('click', closeModal));

addToCartBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const productId = btn.getAttribute('data-product-id');
        const pName = btn.getAttribute('data-product-name');
        const pPrice = btn.getAttribute('data-product-price');
        const pImg = btn.getAttribute('data-product-img');
        
        if(!productId) return;

        summaryImg.src = pImg;
        summaryName.textContent = pName;
        summaryPrice.textContent = pPrice;

        recGrid.innerHTML = '<p style="grid-column:1/-1; text-align:center; color:#666;">Finding the best matches for you...</p>';
        recModal.classList.add('active');

        fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            recGrid.innerHTML = ''; 

            // --- NEW: Add the "See Calculation" Link ---
            const calcLink = document.createElement('a');
            calcLink.href = `/explain?id=${productId}`;
            calcLink.target = "_blank";
            calcLink.innerText = "How is this calculated?";
            calcLink.style.display = "block";
            calcLink.style.gridColumn = "1/-1";
            calcLink.style.textAlign = "right";
            calcLink.style.fontSize = "0.8rem";
            calcLink.style.color = "#aaa";
            calcLink.style.textDecoration = "underline";
            calcLink.style.marginBottom = "10px";
            recGrid.appendChild(calcLink);
            // --------------------------------------------

            if (data.length === 0) {
                recGrid.innerHTML += '<p style="grid-column:1/-1; text-align:center; color:#888;">No specific recommendations found for this item.</p>';
                return;
            }

            data.forEach(item => {
                // Added Score Badge
                const itemHTML = `
                    <div class="rec-item" style="position:relative;">
                        <span style="position:absolute; top:5px; left:5px; background:#22c55e; color:white; font-size:0.7rem; padding:2px 5px; border-radius:3px;">
                            ${item.score}% Match
                        </span>
                        <img src="/static/images/products/${item.image}" alt="${item.name}">
                        <div class="rec-title">${item.name}</div>
                        <div class="rec-price">$${item.price}</div>
                        <button class="rec-add-btn">Add</button>
                    </div>
                `;
                recGrid.innerHTML += itemHTML;
            });
        })
        .catch(error => {
            console.error('Error:', error);
            recGrid.innerHTML = '<p style="color:red; text-align:center; grid-column:1/-1;">Error loading recommendations.</p>';
        });
    });
});