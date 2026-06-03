// Chart instances
let inventoryChart = null;
let trendsChart = null;

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadInventoryChart();
    loadDonationTrends();
    loadUnreadNotificationsCount();
    
    // Auto-refresh every 30 seconds
    setInterval(function() {
        loadInventoryChart();
        loadDonationTrends();
    }, 30000);
    
    // Add event listeners for role-specific actions
    setupEventListeners();
});

function loadInventoryChart() {
    fetch('/api/inventory')
        .then(response => response.json())
        .then(data => {
            const bloodTypes = data.map(item => item.blood_type);
            const quantities = data.map(item => item.quantity);
            const colors = quantities.map(q => q < 10 ? '#dc3545' : '#28a745');
            
            const ctx = document.getElementById('inventoryChart').getContext('2d');
            
            if (inventoryChart) {
                inventoryChart.destroy();
            }
            
            inventoryChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: bloodTypes,
                    datasets: [{
                        label: 'Blood Units Available',
                        data: quantities,
                        backgroundColor: colors,
                        borderColor: colors.map(c => c.replace('0.6', '1')),
                        borderWidth: 1,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    let value = context.raw;
                                    let threshold = data[context.dataIndex].critical_threshold;
                                    label += `: ${value} units`;
                                    if (value < threshold) {
                                        label += ` (⚠️ Below threshold of ${threshold})`;
                                    }
                                    return label;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Units Available'
                            }
                        }
                    }
                }
            });
            
            // Update total units and shortage count
            const totalUnits = quantities.reduce((a, b) => a + b, 0);
            const shortageCount = quantities.filter(q => q < 10).length;
            
            if (document.getElementById('total-units')) {
                document.getElementById('total-units').innerText = totalUnits;
            }
            if (document.getElementById('shortage-count')) {
                document.getElementById('shortage-count').innerText = shortageCount;
            }
        })
        .catch(error => console.error('Error loading inventory:', error));
}

function loadDonationTrends() {
    fetch('/api/donation_trends')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('trendsChart').getContext('2d');
            
            if (trendsChart) {
                trendsChart.destroy();
            }
            
            trendsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Daily Donations (Units)',
                        data: data.counts,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#dc3545',
                        pointBorderColor: '#fff',
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `Donations: ${context.raw} units`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Units Donated'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            },
                            ticks: {
                                maxRotation: 45,
                                minRotation: 45,
                                autoSkip: true,
                                maxTicksLimit: 10
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading trends:', error));
}

function loadUnreadNotificationsCount() {
    fetch('/api/unread_notifications_count')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notification-count');
            if (badge) {
                if (data.count > 0) {
                    badge.innerText = data.count;
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(error => console.error('Error loading notifications:', error));
}

function fulfillRequest(requestId) {
    if (confirm('Are you sure you want to fulfill this emergency request? This will deduct blood from inventory.')) {
        fetch(`/api/respond_request/${requestId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Success', data.message, 'success');
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                showNotification('Error', data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error', 'An error occurred while fulfilling the request', 'danger');
        });
    }
}

function showNotification(title, message, type) {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-notification';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.innerHTML = `
        <strong>${title}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.getElementById('toast-container').appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function setupEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('global-search');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = this.value;
                if (query) {
                    window.location.href = `/search?q=${encodeURIComponent(query)}`;
                }
            }
        });
    }
    
    // Auto-refresh inventory display
    const inventoryCards = document.querySelectorAll('.inventory-card');
    if (inventoryCards.length > 0) {
        setInterval(() => {
            loadInventoryChart();
        }, 60000);
    }
}

// Export functions for global use
window.fulfillRequest = fulfillRequest;
window.showNotification = showNotification;