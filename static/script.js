function runForecast() {
    fetch('/run_query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            route: 'NBO-DXB',
            flight_date: '2026-05-01',
            fare: 500
        })
    })
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById('chart'), {
            type: 'bar',
            data: {
                labels: ['Demand', 'Revenue'],
                datasets: [{
                    data: [data.demand, data.revenue]
                }]
            }
        });
    });
}
