document.addEventListener('DOMContentLoaded', function() {

    const productItems = document.querySelectorAll('.game-card, .related-game-card');

    const hoverBox = document.createElement('div');
    hoverBox.className = 'hover-description';
    hoverBox.innerHTML = '<div class="hover-content"><div class="hover-loading">Loading...</div></div>';
    document.body.appendChild(hoverBox);

    let isHovering = false;0
    let hoverTimeout;
    let currentGameId = null;
    
    productItems.forEach(item => {
        const link = item.querySelector('a');
        if (!link) return;
        
        const href = link.getAttribute('href');
        const gameId = href.split('/').pop();
        
        item.addEventListener('mouseenter', function(e) {
            isHovering = true;
            currentGameId = gameId;
            
            clearTimeout(hoverTimeout);
            
            hoverTimeout = setTimeout(() => {
                if (!isHovering) return;
                
                positionHoverBox(e);
                
                hoverBox.style.display = 'block';
                
                fetch(`/api/game/${gameId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (isHovering && currentGameId === gameId) {
                            hoverBox.innerHTML = `
                                <div class="hover-content">
                                    <h3>${data.name}</h3>
                                    <div class="hover-meta">
                                        <span class="hover-price">${data.price}</span>
                                        <span class="hover-platform">${data.platform}</span>
                                    </div>
                                    <p class="hover-desc">${data.description}</p>
                                    <div class="hover-impact">Impact: ${data.impact || 'N/A'}</div>
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        console.error("Error fetching game details:", error);
                        hoverBox.innerHTML = '<div class="hover-content">Unable to load description</div>';
                    });
            }, 300);
        });
        
        item.addEventListener('mouseleave', function() {
            isHovering = false;
            currentGameId = null;
            clearTimeout(hoverTimeout);
            
            hoverBox.style.display = 'none';
        });
        
        item.addEventListener('mousemove', function(e) {
            if (isHovering) {
                positionHoverBox(e);
            }
        });
    });
    
    function positionHoverBox(e) {
        const mouseX = e.clientX;
        const mouseY = e.clientY;
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        
        const boxWidth = 300;
        const boxHeight = 200;
        
        let left = mouseX + 15;
        let top = mouseY + 15;
        
        if (left + boxWidth > windowWidth - 20) {
            left = mouseX - boxWidth - 15;
        }
        
        if (top + boxHeight > windowHeight - 20) {
            top = windowHeight - boxHeight - 20;
        }
        
        hoverBox.style.left = `${left}px`;
        hoverBox.style.top = `${top}px`;
    }
});