document.addEventListener('DOMContentLoaded', () => {
  const video = document.getElementById('videoReconhecer');
  const status = document.getElementById('status');

  let modelosCarregados = false;
  let streamAtivo = null;
  let intervalId = null;

  // Mostra a área de reconhecimento facial e esconde o menu
  function mostrarFaceArea() {
    document.getElementById("menuOpcoes").style.display = "none";
    document.getElementById("faceArea").style.display = "block";
  }

  // Inicia o reconhecimento facial
  async function iniciarReconhecimento() {
    if (modelosCarregados) return;

    modelosCarregados = true;

    // Carrega os modelos da IA usados pelo face-api.js
    await faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models');
    await faceapi.nets.faceLandmark68Net.loadFromUri('/static/models');
    await faceapi.nets.faceRecognitionNet.loadFromUri('/static/models');

    // Liga a câmera — pode pedir permissão ao usuário
    try {
      streamAtivo = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = streamAtivo;
      await video.play();
      status.textContent = 'Câmera ligada. Detectando rosto...';
    } catch (err) {
      status.textContent = 'Erro ao acessar a câmera: ' + err;
      return;
    }

    // Aguarda a câmera informar tamanho real (videoWidth/Height)
    await new Promise(resolve => {
      if (video.readyState >= 1) return resolve();
      video.addEventListener('loadedmetadata', () => resolve(), { once: true });
    });

    // Criar canvas corretamente após metadata
    const canvas = faceapi.createCanvasFromMedia(video);
    // Garantir que o container permita posicionamento absoluto:
    video.parentElement.style.position = 'relative';
    canvas.style.position = 'absolute';
    canvas.style.top = video.offsetTop + 'px';
    canvas.style.left = video.offsetLeft + 'px';
    // Ajustar tamanho do canvas para o size real do vídeo
    const displaySize = { width: video.videoWidth, height: video.videoHeight };
    faceapi.matchDimensions(canvas, displaySize);
    video.parentElement.appendChild(canvas);

    let reconhecendo = false;

    async function verificarFrame() {
      if (reconhecendo) return;
      reconhecendo = true;
      // Detecta rosto, landmarks e gera o "descriptor" (a impressão digital do rosto)
      const detections = await faceapi
        .detectSingleFace(video)
        .withFaceLandmarks()
        .withFaceDescriptor();

      // Limpa o canvas a cada frame
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Se não encontrou rosto
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

        // Compara cada descriptor do banco com o do vídeo
        moradores.forEach(m => {
          if (!m.descriptor) return;
          const dist = Math.sqrt(
            m.descriptor.reduce((sum, val, i) => sum + (val - descriptor[i]) ** 2, 0)
          );
          if (dist < melhor.distance) melhor = { nome: m.nome, distance: dist };
        });

        // Rosto encontrado e reconhecido
        if (melhor.distance <= threshold) {
          status.textContent = `✅ ACESSO LIBERADO: ${melhor.nome}`;

          // Envia registro do acesso para o backend
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

  // ACESSO POR CÓDIGO — Visitante
document.getElementById("confirmarCodigo").onclick = async () => {
    const codigo = document.getElementById("codigoInput").value;
    const statusCodigo = document.getElementById("codigoStatus");

    if (!codigo) {
      statusCodigo.textContent = "Digite um código!";
      return;
    }

    try {
      // Envia o código para validação na rota Python
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
  // Esconde a área de código
  document.getElementById("codigoArea").style.display = "none";
  // Mostra o menu principal
  document.getElementById("menuOpcoes").style.display = "flex"; // ou "block"
};

});

