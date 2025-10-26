const rawData = JSON.parse(document.getElementById('chart-data').textContent);

const groupedData = {};
rawData.forEach(item => {
    const [region, district, population] = item;
    if (!groupedData[region]) groupedData[region] = [];
    groupedData[region].push([district, parseInt(population, 10)]);
});

const regions = Object.keys(groupedData).sort();
const regionList = document.getElementById('regionList');
const chartsGrid = document.getElementById('chartsGrid');
const toggleAllBtn = document.getElementById('toggleAll');
const modal = document.getElementById('detailModal');
const modalTitle = document.getElementById('modalTitle');
const modalChartCtx = document.getElementById('modalChart').getContext('2d');

const chartInstances = {};
let modalChartInstance = null;
let allCollapsed = false;

regions.forEach(region => {
    const div = document.createElement('div');
    div.className = 'region-item';
    div.innerHTML = `
                <input type="checkbox" id="check-${region}" checked data-region="${region}">
                <label for="check-${region}">${region}</label>
            `;
    regionList.appendChild(div);
});

regions.forEach(region => {
    const data = groupedData[region];
    const labels = data.map(d => d[0]);
    const values = data.map(d => d[1]);

    const card = document.createElement('div');
    card.className = 'chart-card';
    card.id = `card-${region}`;
    card.innerHTML = `
                <h3>${region}</h3>
                <div class="chart-wrapper">
                    <canvas id="chart-${region}"></canvas>
                </div>
                <button class="detail-btn" data-region="${region}" title="Детальний перегляд">
                    <i data-feather="eye"></i>
                </button>
            `;
    chartsGrid.appendChild(card);

    const ctx = document.getElementById(`chart-${region}`).getContext('2d');
    chartInstances[region] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Значення',
                data: values,
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {display: false},
                tooltip: {callbacks: {label: ctx => `Значення: ${ctx.parsed.y.toLocaleString('uk-UA')}`}}
            },
            scales: {
                x: {ticks: {autoSkip: false, maxRotation: 90, minRotation: 45, font: {size: 10}}},
                y: {beginAtZero: true, ticks: {callback: v => v.toLocaleString('uk-UA')}}
            }
        }
    });
});

document.querySelectorAll('.detail-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const region = btn.dataset.region;
        const data = groupedData[region];
        const labels = data.map(d => d[0]);
        const values = data.map(d => d[1]);

        modalTitle.textContent = `${region} — Детальний графік`;

        if (modalChartInstance) modalChartInstance.destroy();

        modalChartInstance = new Chart(modalChartCtx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Значення',
                    data: values,
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    tooltip: {callbacks: {label: ctx => `Значення: ${ctx.parsed.y.toLocaleString('uk-UA')}`}}
                },
                scales: {
                    x: {ticks: {autoSkip: false, maxRotation: 90, minRotation: 45, font: {size: 12}}},
                    y: {beginAtZero: true, ticks: {callback: v => v.toLocaleString('uk-UA'), font: {size: 12}}}
                }
            }
        });

        modal.classList.add('active');
    });
});

document.getElementById('closeModal').addEventListener('click', () => {
    modal.classList.remove('active');
});

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('active');
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        modal.classList.remove('active');
    }
});

document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        const region = checkbox.dataset.region;
        const card = document.getElementById(`card-${region}`);
        card.classList.toggle('hidden', !checkbox.checked);
    });
});

toggleAllBtn.addEventListener('click', () => {
    allCollapsed = !allCollapsed;
    toggleAllBtn.textContent = allCollapsed ? 'Show all' : 'Hide all';
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.checked = !allCollapsed;
        const card = document.getElementById(`card-${cb.dataset.region}`);
        card.classList.toggle('hidden', allCollapsed);
    });
});

feather.replace();
