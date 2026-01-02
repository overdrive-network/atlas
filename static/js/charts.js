// Chart.js configurations and data loading
let metricsData = null;

// Constants
const NOT_AVAILABLE = 'N/A';

// Load metrics on page load
window.addEventListener('DOMContentLoaded', () => {
    loadMetrics();
});

async function loadMetrics() {
    const loading = document.getElementById('loading');
    const content = document.getElementById('dashboard-content');
    const errorDiv = document.getElementById('error-message');

    try {
        const response = await fetch('/api/metrics');
        
        if (!response.ok) {
            throw new Error('Failed to fetch metrics');
        }

        metricsData = await response.json();
        
        // Hide loading, show content
        loading.style.display = 'none';
        content.style.display = 'block';

        // Update today's stats
        updateTodayStats(metricsData.today);

        // Create charts
        createCharts(metricsData.week);

    } catch (error) {
        console.error('Error loading metrics:', error);
        loading.style.display = 'none';
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Failed to load health data: ' + error.message;
    }
}

function updateTodayStats(today) {
    // Update steps
    const steps = today.steps || 0;
    document.getElementById('steps-today').textContent = steps.toLocaleString();

    // Update heart rate
    const heartRate = today.heart_rate?.restingHeartRate || NOT_AVAILABLE;
    document.getElementById('heart-rate-today').textContent = 
        heartRate !== NOT_AVAILABLE ? heartRate + ' bpm' : heartRate;

    // Update sleep
    const sleepHours = today.sleep?.total_hours || 0;
    document.getElementById('sleep-today').textContent = sleepHours.toFixed(1) + 'h';

    // Update calories
    const calories = today.calories || 0;
    document.getElementById('calories-today').textContent = calories.toLocaleString();
}

function createCharts(weekData) {
    if (!weekData || weekData.length === 0) {
        return;
    }

    // Sort by date (oldest first for chart display)
    weekData.sort((a, b) => new Date(a.date) - new Date(b.date));

    // Extract data for charts
    const dates = weekData.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const steps = weekData.map(d => d.steps || 0);
    const sleepHours = weekData.map(d => d.sleep_hours || 0);
    const distance = weekData.map(d => d.distance || 0);
    const calories = weekData.map(d => d.calories || 0);

    // Steps Chart
    createChart('stepsChart', 'line', {
        labels: dates,
        datasets: [{
            label: 'Steps',
            data: steps,
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4,
            fill: true
        }]
    }, 'Steps');

    // Sleep Chart
    createChart('sleepChart', 'bar', {
        labels: dates,
        datasets: [{
            label: 'Sleep (hours)',
            data: sleepHours,
            backgroundColor: '#764ba2',
            borderRadius: 8
        }]
    }, 'Hours');

    // Distance Chart
    createChart('distanceChart', 'line', {
        labels: dates,
        datasets: [{
            label: 'Distance (km)',
            data: distance,
            borderColor: '#f093fb',
            backgroundColor: 'rgba(240, 147, 251, 0.1)',
            tension: 0.4,
            fill: true
        }]
    }, 'Kilometers');

    // Calories Chart
    createChart('caloriesChart', 'bar', {
        labels: dates,
        datasets: [{
            label: 'Calories Burned',
            data: calories,
            backgroundColor: '#fa709a',
            borderRadius: 8
        }]
    }, 'Calories');
}

function createChart(canvasId, type, data, yAxisLabel) {
    const ctx = document.getElementById(canvasId);
    
    if (!ctx) {
        console.error(`Canvas element ${canvasId} not found`);
        return;
    }

    new Chart(ctx, {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    },
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            size: 12
                        }
                    },
                    title: {
                        display: true,
                        text: yAxisLabel,
                        font: {
                            size: 13,
                            weight: 'bold'
                        }
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}
