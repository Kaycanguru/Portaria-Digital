document.addEventListener('DOMContentLoaded', async () => {
  const ctxAcessos = document.getElementById('acessosChart').getContext('2d');

  try {
    const res = await fetch('/dashboard/dados_grafico');
    const data = await res.json();

    // 🔹 Cria um array de cores alternando azul e roxo
    const cores = data.valores.map((_, i) => i % 2 === 0 ? '#28044C' : '#E4D8FF');

    new Chart(ctxAcessos, {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Total de Acessos',
          data: data.valores,
          backgroundColor: cores,
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  } catch (err) {
    console.error('Erro ao carregar gráfico:', err);
  }
});
