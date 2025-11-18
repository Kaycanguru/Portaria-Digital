document.addEventListener('DOMContentLoaded', () => {
  const video = document.getElementById('videoReconhecer');
  const status = document.getElementById('status');

  let modelosCarregados = false;
  let streamAtivo = null;
  let intervalId = null;

  // mostra a área do reconhecimento (esconde menu) e inicia o processo
  function mostrarFaceArea() {
    document.getElementById("menuOpcoes").style.display = "none";
    document.getElementById("faceArea").style.display = "block";
  }

  async function iniciarReconhecimento() {
    if (modelosCarregados) return;

    modelosCarregados = true;

    // carrega modelos
    await faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models');
    await faceapi.nets.faceLandmark68Net.loadFromUri('/static/models');
    await faceapi.nets.faceRecognitionNet.loadFromUri('/static/models');

    // iniciar câmera
    try {
      streamAtivo = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = streamAtivo;
      await video.play();
      status.textContent = 'Câmera ligada. Detectando rosto...';
    } catch (err) {
      status.textContent = 'Erro ao acessar a câmera: ' + err;
      return;
    }

    // aguardar metadata para garantir video.videoWidth/videoHeight corretos
    await new Promise(resolve => {
      if (video.readyState >= 1) return resolve();
      video.addEventListener('loadedmetadata', () => resolve(), { once: true });
    });

    // criar canvas corretamente após metadata
    const canvas = faceapi.createCanvasFromMedia(video);
    // garantir que o container permita posicionamento absoluto:
    video.parentElement.style.position = 'relative';
    canvas.style.position = 'absolute';
    canvas.style.top = video.offsetTop + 'px';
    canvas.style.left = video.offsetLeft + 'px';
    // ajustar tamanho do canvas para o size real do vídeo
    const displaySize = { width: video.videoWidth, height: video.videoHeight };
    faceapi.matchDimensions(canvas, displaySize);
    video.parentElement.appendChild(canvas);

    let reconhecendo = false;

    async function verificarFrame() {
      if (reconhecendo) return;
      reconhecendo = true;

      const detections = await faceapi
        .detectSingleFace(video)
        .withFaceLandmarks()
        .withFaceDescriptor();

      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (!detections) {
        status.textContent = 'Aguardando rosto...';
        reconhecendo = false;
        return;
      }

      try {
        const res = await fetch('/moradores/descriptors');
        if (!res.ok) throw new Error('Erro ao buscar descritores.');
        const moradores = await res.json();

        const descriptor = Array.from(detections.descriptor);
        const threshold = 0.6;

        let melhor = { nome: null, distance: Infinity };
        moradores.forEach(m => {
          if (!m.descriptor) return;
          const dist = Math.sqrt(
            m.descriptor.reduce((sum, val, i) => sum + (val - descriptor[i]) ** 2, 0)
          );
          if (dist < melhor.distance) melhor = { nome: m.nome, distance: dist };
        });

        if (melhor.distance <= threshold) {
          status.textContent = `✅ ACESSO LIBERADO: ${melhor.nome}`;

          // envia registro (async fire-and-forget)
          fetch('/reconhecer/registrar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome: melhor.nome })
          }).catch(e => console.error('Erro registrar:', e));
        } else {
          status.textContent = `⛔ Acesso negado`;
        }

      } catch (err) {
        status.textContent = err.message;
      }

      setTimeout(() => (reconhecendo = false), 3000);
    }

    // limpa interval antigo (se houver) e cria um novo
    if (intervalId) clearInterval(intervalId);
    intervalId = setInterval(verificarFrame, 1000);
  }

  // função pública chamada pelo botão: mostra a tela e inicia tudo
  window.abrirFacial = () => {
    mostrarFaceArea();
    iniciarReconhecimento();
  };

  // --- ACESSO POR CÓDIGO ---
document.getElementById("confirmarCodigo").onclick = async () => {
    const codigo = document.getElementById("codigoInput").value;
    const statusCodigo = document.getElementById("codigoStatus");

    if (!codigo) {
      statusCodigo.textContent = "Digite um código!";
      return;
    }

    try {
      const res = await fetch('http://127.0.0.1:5000/reconhecer/codigo', {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ codigo })
      });

      const data = await res.json();
      statusCodigo.textContent = data.message;
    } catch (err) {
      statusCodigo.textContent = 'Erro ao conectar: ' + err.message;
    }
};

// Botão "Voltar"
document.getElementById("voltarCodigo").onclick = () => {
  // esconde a área de código
  document.getElementById("codigoArea").style.display = "none";
  // mostra o menu principal
  document.getElementById("menuOpcoes").style.display = "flex"; // ou "block"
};

});

