// elementos existentes
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('captureBtn');
const preview = document.getElementById('preview');
const descriptorInput = document.getElementById('face_descriptor');

async function loadModels() {
  // espera carregar modelos (apontando para /static/models)
  await faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('/static/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/static/models');
}

// inicia webcam
async function start() {
  await loadModels();
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => alert("Erro ao acessar a câmera: " + err));
}

start();
// captura a foto
captureBtn.addEventListener('click', async () => {
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL('image/png'); // base64
  preview.src = dataURL;
  preview.style.display = 'block';

  // Detecta qual hidden input existe na página (morador)
  const hiddenInput = document.getElementById('foto_morador_data');
  
  if(hiddenInput) hiddenInput.value = dataURL;

  // calcula descritor
  const img = await faceapi.fetchImage(dataURL);
  const singleResult = await faceapi.detectSingleFace(img)
                                   .withFaceLandmarks()
                                   .withFaceDescriptor();

  if (!singleResult) {
    alert('Não foi detectado rosto. Tente novamente.');
    descriptorInput.value = '';
    return;
  }

  const descriptor = Array.from(singleResult.descriptor); // converte Float32Array para array normal
  descriptorInput.value = JSON.stringify(descriptor); // envia para backend
});
