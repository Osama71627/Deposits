class DashboardCharts {
    constructor() {
        this.initCharts();
    }

    initCharts() {
        this.renderRevenueChart();
        this.renderRequestsChart();
        this.renderWarehouseChart();
        this.renderCourierChart();
    }

    renderRevenueChart() {
        const canvas = document.getElementById('revenueChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(99, 102, 241, 0.2)');
        gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');

        const months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'];
        const data = [45000, 52000, 48000, 58000, 62000, 55000, 67000, 72000, 68000, 75000, 82000, 78000];
        
        const width = canvas.parentElement.clientWidth;
        const height = 280;
        canvas.width = width * 2;
        canvas.height = height * 2;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        ctx.scale(2, 2);

        const padding = { top: 20, right: 20, bottom: 40, left: 60 };
        const chartW = width - padding.left - padding.right;
        const chartH = height - padding.top - padding.bottom;
        
        const maxVal = Math.max(...data) * 1.1;
        const minVal = 0;
        const stepY = (maxVal - minVal) / 5;
        const stepX = chartW / (data.length - 1);

        ctx.clearRect(0, 0, width, height);

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? '#94a3b8' : '#64748b';
        const gridColor = isDark ? '#334155' : '#e2e8f0';
        const lineColor = '#6366f1';

        ctx.strokeStyle = gridColor;
        ctx.lineWidth = 1;
        for (let i = 0; i <= 5; i++) {
            const y = padding.top + (chartH / 5) * i;
            ctx.beginPath();
            ctx.moveTo(padding.left, y);
            ctx.lineTo(width - padding.right, y);
            ctx.stroke();

            const val = maxVal - (maxVal / 5) * i;
            ctx.fillStyle = textColor;
            ctx.font = '11px sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(val >= 1000 ? (val / 1000).toFixed(0) + 'K' : val.toFixed(0), padding.left - 10, y + 4);
        }

        const points = data.map((val, i) => ({
            x: padding.left + stepX * i,
            y: padding.top + chartH - ((val - minVal) / (maxVal - minVal)) * chartH
        }));

        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
            const cp1x = (points[i-1].x + points[i].x) / 2;
            const cp1y = points[i-1].y;
            const cp2x = cp1x;
            const cp2y = points[i].y;
            ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, points[i].x, points[i].y);
        }
        ctx.strokeStyle = lineColor;
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.lineTo(points[points.length-1].x, padding.top + chartH);
        ctx.lineTo(points[0].x, padding.top + chartH);
        ctx.closePath();
        ctx.fillStyle = gradient;
        ctx.fill();

        points.forEach((p, i) => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#fff';
            ctx.fill();
            ctx.strokeStyle = lineColor;
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.fillStyle = textColor;
            ctx.font = '11px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(months[i], p.x, height - 5);
        });
    }

    renderRequestsChart() {
        const canvas = document.getElementById('requestsChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        const days = ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'];
        const pending = [12, 8, 15, 10, 18, 14, 6];
        const completed = [25, 30, 22, 28, 35, 20, 15];

        const width = canvas.parentElement.clientWidth;
        const height = 250;
        canvas.width = width * 2;
        canvas.height = height * 2;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        ctx.scale(2, 2);

        const padding = { top: 20, right: 20, bottom: 40, left: 40 };
        const chartW = width - padding.left - padding.right;
        const chartH = height - padding.top - padding.bottom;
        const barW = chartW / (days.length * 2.5);

        const maxVal = Math.max(...pending, ...completed) * 1.2;
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? '#94a3b8' : '#64748b';

        ctx.clearRect(0, 0, width, height);

        days.forEach((day, i) => {
            const x = padding.left + (chartW / days.length) * i + (chartW / days.length - barW * 2) / 2;

            const h1 = (pending[i] / maxVal) * chartH;
            ctx.fillStyle = '#f59e0b';
            ctx.roundRect ? ctx.roundRect(x, padding.top + chartH - h1, barW, h1, 4) : ctx.fillRect(x, padding.top + chartH - h1, barW, h1);
            ctx.fill();

            const h2 = (completed[i] / maxVal) * chartH;
            ctx.fillStyle = '#10b981';
            ctx.roundRect ? ctx.roundRect(x + barW + 4, padding.top + chartH - h2, barW, h2, 4) : ctx.fillRect(x + barW + 4, padding.top + chartH - h2, barW, h2);
            ctx.fill();

            ctx.fillStyle = textColor;
            ctx.font = '11px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(day, x + barW + 2, height - 5);
        });

        ctx.fillStyle = textColor;
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('■ معلق', padding.left, 12);
        ctx.fillStyle = '#10b981';
        ctx.fillText('■ مكتمل', padding.left + 80, 12);
    }

    renderWarehouseChart() {
        const canvas = document.getElementById('warehouseChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        const data = [
            { label: 'مستودع الرياض', used: 820, total: 1000 },
            { label: 'مستودع جدة', used: 450, total: 800 },
            { label: 'مستودع boulevard', used: 680, total: 750 },
        ];

        const width = 320;
        const height = 180;
        canvas.width = width * 2;
        canvas.height = height * 2;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        ctx.scale(2, 2);

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? '#94a3b8' : '#64748b';

        ctx.clearRect(0, 0, width, height);

        data.forEach((item, i) => {
            const y = 20 + i * 50;
            const pct = (item.used / item.total) * 100;
            const barW = (pct / 100) * (width - 120);

            ctx.fillStyle = textColor;
            ctx.font = '12px sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(item.label, 100, y + 14);

            ctx.fillStyle = isDark ? '#334155' : '#e2e8f0';
            ctx.beginPath();
            if (ctx.roundRect) {
                ctx.roundRect(120, y, width - 120, 16, 8);
            } else {
                ctx.fillRect(120, y, width - 120, 16);
            }
            ctx.fill();

            const colors = ['#6366f1', '#06b6d4', '#f59e0b'];
            ctx.fillStyle = colors[i];
            ctx.beginPath();
            if (ctx.roundRect) {
                ctx.roundRect(120, y, barW, 16, 8);
            } else {
                ctx.fillRect(120, y, barW, 16);
            }
            ctx.fill();

            ctx.fillStyle = textColor;
            ctx.font = '11px sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText(pct.toFixed(0) + '%', width - 12, y + 14);
        });
    }

    renderCourierChart() {
        const canvas = document.getElementById('courierChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        const data = [85, 72, 90, 65, 78, 88, 70];
        const labels = ['أحمد', 'سارة', 'خالد', 'نورة', 'فيصل', 'مريم', 'عمر'];

        const width = 300;
        const height = 200;
        canvas.width = width * 2;
        canvas.height = height * 2;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        ctx.scale(2, 2);

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? '#94a3b8' : '#64748b';

        ctx.clearRect(0, 0, width, height);

        const padding = { top: 10, right: 40, bottom: 30, left: 40 };
        const chartW = width - padding.left - padding.right;
        const chartH = height - padding.top - padding.bottom;
        const centerX = padding.left + chartW / 2;
        const centerY = padding.top + chartH / 2;
        const radius = Math.min(chartW, chartH) / 2;

        const total = data.reduce((a, b) => a + b, 0);
        let startAngle = -Math.PI / 2;

        const colors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

        data.forEach((val, i) => {
            const sliceAngle = (val / total) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
            ctx.closePath();
            ctx.fillStyle = colors[i];
            ctx.fill();
            startAngle += sliceAngle;

            const labelAngle = startAngle - sliceAngle / 2;
            const labelR = radius + 15;
            const lx = centerX + Math.cos(labelAngle) * labelR;
            const ly = centerY + Math.sin(labelAngle) * labelR;

            ctx.fillStyle = textColor;
            ctx.font = '10px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(labels[i], lx, ly + 3);
        });

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = isDark ? '#1e293b' : '#ffffff';
        ctx.fill();

        ctx.fillStyle = textColor;
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('التقييم', centerX, centerY - 5);
        ctx.fillStyle = isDark ? '#f1f5f9' : '#0f172a';
        ctx.font = '18px sans-serif';
        ctx.fontWeight = 'bold';
        ctx.fillText('4.8', centerX, centerY + 18);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => new DashboardCharts(), 100);
});
