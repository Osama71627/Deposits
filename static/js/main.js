class DepositsApp {
    constructor() {
        this.initTheme();
        this.initSidebar();
        this.initNotifications();
        this.initSearch();
        this.loadDashboardData();
    }

    initTheme() {
        const saved = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', saved);
        
        document.querySelectorAll('.theme-toggle').forEach(el => {
            el.addEventListener('click', () => {
                const current = document.documentElement.getAttribute('data-theme');
                const next = current === 'dark' ? 'light' : 'dark';
                document.documentElement.setAttribute('data-theme', next);
                localStorage.setItem('theme', next);
                el.querySelector('i').className = next === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            });
        });
    }

    initSidebar() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (e.currentTarget.tagName === 'A') return;
                document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
                item.classList.add('active');
            });
        });

        const toggleBtn = document.getElementById('sidebarToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                document.querySelector('.sidebar').classList.toggle('open');
            });
        }
    }

    initNotifications() {
        document.querySelectorAll('.notification-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const dropdown = btn.nextElementSibling;
                if (dropdown) dropdown.classList.toggle('show');
            });
        });
    }

    initSearch() {
        const searchInputs = document.querySelectorAll('.navbar-search input');
        searchInputs.forEach(input => {
            input.addEventListener('keyup', (e) => {
                const query = e.target.value.toLowerCase();
                document.querySelectorAll('.searchable-row').forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(query) ? '' : 'none';
                });
            });
        });
    }

    async loadDashboardData() {
        try {
            const response = await fetch('/api/analytics/dashboard/');
            if (response.ok) {
                const data = await response.json();
                this.updateStats(data);
            }
        } catch (err) {
            console.log('Dashboard data will load when API is ready');
        }
    }

    updateStats(data) {
        const statValues = document.querySelectorAll('[data-stat]');
        statValues.forEach(el => {
            const key = el.dataset.stat;
            if (data[key] !== undefined) {
                const val = data[key];
                el.textContent = typeof val === 'number' && val > 1000 
                    ? val.toLocaleString() 
                    : val;
            }
        });
    }

    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} fade-in`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
        }

    formatDate(dateStr) {
        return new Date(dateStr).toLocaleDateString('ar-SA', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('ar-SA', {
            style: 'currency',
            currency: 'SAR'
        }).format(amount);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new DepositsApp();
});
