document.addEventListener('DOMContentLoaded', async () => {
  const ctxAcessos = document.getElementById('acessosChart').getContext('2d');

  try {
    const res = await fetch('/dashboard/dados_grafico'); // Busca a rota python
    const data = await res.json();
    // Cria um array de cores alternando entre roxo claro e escuro
    const cores = data.valores.map((_, i) => i % 2 === 0 ? '#28044C' : '#E4D8FF');

    // Cria o gráfico Chart.js
    new Chart(ctxAcessos, {
      type: 'bar',
      data: {
        labels: data.labels, // labels - datas
        datasets: [{
          label: 'Total de Acessos',
          data: data.valores, // quantidades
          backgroundColor: cores, // cores alternadas
          borderRadius: 6
        }]
      },
      options: { // configuração detalhada do gráfico
        responsive: true,
        scales: {
          y: {
            beginAtZero: true, // começa do zero (eixo y)
            ticks: { stepSize: 1 } // escala sobre de 1 em 1
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
