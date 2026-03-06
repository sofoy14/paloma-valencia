// Dashboard para Vercel - Sin backend persistente, todo en cliente
const API_URL = '/api';

// Estado global
let articles = [];
let currentFilter = 'all';

// Fetch noticias al cargar
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard Vercel cargado');
    loadNews();
    // Refrescar cada 5 minutos
    setInterval(loadNews, 5 * 60 * 1000);
});

async function loadNews() {
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/news`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await response.json();
        articles = data.articles || [];
        
        // Guardar en localStorage para persistencia
        localStorage.setItem('paloma_news', JSON.stringify(articles));
        localStorage.setItem('last_update', new Date().toISOString());
        
        renderArticles();
        updateStats();
        
    } catch (error) {
        console.error('Error cargando noticias:', error);
        // Intentar cargar de localStorage
        const cached = localStorage.getItem('paloma_news');
        if (cached) {
            articles = JSON.parse(cached);
            renderArticles();
            showNotification('Usando datos en caché', 'warning');
        } else {
            showError('No se pudieron cargar las noticias');
        }
    }
}

function showLoading() {
    document.getElementById('articles-list').innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Cargando noticias...</p>
        </div>
    `;
}

function renderArticles() {
    const container = document.getElementById('articles-list');
    
    if (articles.length === 0) {
        container.innerHTML = '<div class="empty">No hay noticias disponibles</div>';
        return;
    }
    
    let filtered = articles;
    
    if (currentFilter === 'high') {
        filtered = articles.filter(a => (a.relevance_score || 0) >= 30);
    } else if (currentFilter === 'alert') {
        filtered = articles.filter(a => a.is_alert);
    } else if (currentFilter === 'positive') {
        filtered = articles.filter(a => a.sentiment === 'positive');
    } else if (currentFilter === 'negative') {
        filtered = articles.filter(a => a.sentiment === 'negative');
    }
    
    container.innerHTML = filtered.map(article => `
        <div class="article-card ${article.is_alert ? 'alert' : ''}">
            <div class="article-header">
                <span class="badge sentiment-${article.sentiment || 'neutral'}">
                    ${getSentimentEmoji(article.sentiment)}
                </span>
                ${article.relevance_score >= 30 ? `<span class="badge hot">🔥 ${article.relevance_score}</span>` : ''}
                ${article.is_alert ? '<span class="badge alert">🚨 ALERTA</span>' : ''}
            </div>
            <a href="${article.url}" target="_blank" class="article-title">
                ${article.title}
            </a>
            <div class="article-meta">
                <span>📰 ${article.source}</span>
                <span>🕐 ${formatDate(article.published_at)}</span>
            </div>
            ${article.summary ? `<p class="article-summary">${article.summary.substring(0, 150)}...</p>` : ''}
        </div>
    `).join('');
}

function getSentimentEmoji(sentiment) {
    if (sentiment === 'positive') return '✅ Positivo';
    if (sentiment === 'negative') return '⚠️ Negativo';
    return '⚪ Neutral';
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-CO', {hour: '2-digit', minute: '2-digit'});
}

function updateStats() {
    document.getElementById('stat-total').textContent = articles.length;
    document.getElementById('stat-positive').textContent = articles.filter(a => a.sentiment === 'positive').length;
    document.getElementById('stat-negative').textContent = articles.filter(a => a.sentiment === 'negative').length;
    document.getElementById('stat-alerts').textContent = articles.filter(a => a.is_alert).length;
    document.getElementById('stat-high').textContent = articles.filter(a => (a.relevance_score || 0) >= 30).length;
    
    const lastUpdate = localStorage.getItem('last_update');
    if (lastUpdate) {
        document.getElementById('last-update').textContent = 'Última actualización: ' + formatDate(lastUpdate);
    }
}

function filterNews(type) {
    currentFilter = type;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    renderArticles();
}

function refreshNews() {
    loadNews();
    showNotification('Actualizando noticias...', 'info');
}

function showNotification(message, type = 'info') {
    const notif = document.createElement('div');
    notif.className = `notification ${type}`;
    notif.textContent = message;
    document.body.appendChild(notif);
    setTimeout(() => notif.remove(), 3000);
}

function showError(message) {
    document.getElementById('articles-list').innerHTML = `
        <div class="error">
            <h3>⚠️ Error</h3>
            <p>${message}</p>
            <button onclick="loadNews()">Reintentar</button>
        </div>
    `;
}
