(() => {
  const input = document.querySelector('#imageInput');
  const uploadButton = document.querySelector('#uploadButton');
  const replaceButton = document.querySelector('#replaceButton');
  const removeButton = document.querySelector('#removeButton');
  const cameraStart = document.querySelector('#cameraStart');
  const cameraCapture = document.querySelector('#cameraCapture');
  const cameraStop = document.querySelector('#cameraStop');
  const video = document.querySelector('#cameraVideo');
  const preview = document.querySelector('#imagePreview');
  const emptyStage = document.querySelector('#stageEmpty');
  const cameraStatus = document.querySelector('#cameraStatus');
  const analyseButton = document.querySelector('#analyseButton');
  const error = document.querySelector('#uploadError');
  const overlay = document.querySelector('#analysisOverlay');
  const analysisTitle = document.querySelector('#analysisTitle');
  const analysisStep = document.querySelector('#analysisStep');
  const modalLoader = document.querySelector('#modalLoader');
  const modalProgress = document.querySelector('#modalProgress');
  const modalErrorActions = document.querySelector('#modalErrorActions');
  const modalRetryButton = document.querySelector('#modalRetryButton');
  const modalDismissButton = document.querySelector('#modalDismissButton');

  let cameraStream = null;
  let savedImage = '';
  let activeFileBlob = null;
  let statusInterval = null;

  // Centralized API base URL from config.js
  const API_BASE = typeof window.getAyurScanApiBase === 'function'
    ? window.getAyurScanApiBase()
    : '';

  function stopCamera() {
    if (cameraStream) {
      cameraStream.getTracks().forEach((track) => track.stop());
    }
    cameraStream = null;
    video.srcObject = null;
    video.hidden = true;
    cameraStatus.hidden = true;
    cameraCapture.hidden = true;
    cameraStop.hidden = true;
    cameraStart.hidden = false;
  }

  function setPreview(imageData, fileBlob = null) {
    savedImage = imageData;
    activeFileBlob = fileBlob;
    preview.src = imageData;
    preview.hidden = false;
    emptyStage.hidden = true;
    video.hidden = true;
    cameraStatus.hidden = true;
    analyseButton.disabled = false;
    error.textContent = '';

    // Show replace and remove buttons
    if (replaceButton) replaceButton.hidden = false;
    if (removeButton) removeButton.hidden = false;
    uploadButton.hidden = true;

    stopCamera();
  }

  function removePreview() {
    savedImage = '';
    activeFileBlob = null;
    input.value = '';
    preview.hidden = true;
    preview.src = '';
    emptyStage.hidden = false;
    analyseButton.disabled = true;
    error.textContent = '';

    if (replaceButton) replaceButton.hidden = true;
    if (removeButton) removeButton.hidden = true;
    uploadButton.hidden = false;
    stopCamera();
  }

  function compressImage(file) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      const objectUrl = URL.createObjectURL(file);
      image.onload = () => {
        // Allow up to 1600px dimension so multiple small plants retain visual clarity
        const maxDimension = 1600;
        const scale = Math.min(1, maxDimension / Math.max(image.naturalWidth, image.naturalHeight));
        const canvas = document.createElement('canvas');
        canvas.width = Math.round(image.naturalWidth * scale);
        canvas.height = Math.round(image.naturalHeight * scale);
        const ctx = canvas.getContext('2d');
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(objectUrl);

        canvas.toBlob(
          (blob) => {
            if (!blob) {
              reject(new Error('Image compression failed. Try another file.'));
              return;
            }
            const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
            resolve({ dataUrl, blob });
          },
          'image/jpeg',
          0.88
        );
      };
      image.onerror = () => {
        URL.revokeObjectURL(objectUrl);
        reject(new Error('This image could not be opened. Try another photo.'));
      };
      image.src = objectUrl;
    });
  }

  uploadButton.addEventListener('click', () => input.click());
  if (replaceButton) replaceButton.addEventListener('click', () => input.click());
  if (removeButton) removeButton.addEventListener('click', removePreview);

  input.addEventListener('change', async () => {
    const file = input.files && input.files[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      error.textContent = 'Please choose a valid image file (JPEG, PNG, or WEBP).';
      input.value = '';
      return;
    }
    try {
      const result = await compressImage(file);
      setPreview(result.dataUrl, result.blob);
    } catch (reason) {
      error.textContent = reason.message;
    }
  });

  cameraStart.addEventListener('click', async () => {
    error.textContent = '';
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      error.textContent = 'Live camera requires a secure connection (HTTPS or localhost). Please upload a photo instead.';
      return;
    }
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' } },
        audio: false
      });
      video.srcObject = cameraStream;
      video.hidden = false;
      preview.hidden = true;
      emptyStage.hidden = true;
      cameraStatus.hidden = false;
      cameraStart.hidden = true;
      cameraCapture.hidden = false;
      cameraStop.hidden = false;
      if (replaceButton) replaceButton.hidden = true;
      if (removeButton) removeButton.hidden = true;
      uploadButton.hidden = false;
      await video.play();
    } catch (reason) {
      stopCamera();
      error.textContent = reason.name === 'NotAllowedError'
        ? 'Camera permission was denied. Allow camera access or upload a photo.'
        : 'Camera could not be opened. Try uploading a photo instead.';
    }
  });

  cameraStop.addEventListener('click', () => {
    stopCamera();
    if (!savedImage) emptyStage.hidden = false;
    else {
      preview.hidden = false;
      if (replaceButton) replaceButton.hidden = false;
      if (removeButton) removeButton.hidden = false;
      uploadButton.hidden = true;
    }
  });

  cameraCapture.addEventListener('click', () => {
    if (!video.videoWidth || !video.videoHeight) return;
    const canvas = document.createElement('canvas');
    const maxDimension = 1600;
    const scale = Math.min(1, maxDimension / Math.max(video.videoWidth, video.videoHeight));
    canvas.width = Math.round(video.videoWidth * scale);
    canvas.height = Math.round(video.videoHeight * scale);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(
      (blob) => {
        const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
        setPreview(dataUrl, blob);
      },
      'image/jpeg',
      0.88
    );
  });

  // Drag and Drop support
  const stage = document.querySelector('#photoStage');
  stage.addEventListener('dragover', (event) => {
    event.preventDefault();
    stage.classList.add('is-dragging');
  });
  stage.addEventListener('dragleave', () => stage.classList.remove('is-dragging'));
  stage.addEventListener('drop', async (event) => {
    event.preventDefault();
    stage.classList.remove('is-dragging');
    const file = event.dataTransfer.files[0];
    if (!file || !file.type.startsWith('image/')) {
      error.textContent = 'Drop a valid image file to continue.';
      return;
    }
    try {
      const result = await compressImage(file);
      setPreview(result.dataUrl, result.blob);
    } catch (reason) {
      error.textContent = reason.message;
    }
  });

  // Analysis trigger
  analyseButton.addEventListener('click', triggerAnalysis);

  function showAnalyzingOverlay() {
    overlay.classList.add('is-visible');
    overlay.setAttribute('aria-hidden', 'false');
    analyseButton.disabled = true;
    modalLoader.hidden = false;
    modalProgress.hidden = false;
    modalErrorActions.hidden = true;

    analysisTitle.textContent = 'Analyzing your plants...';
    analysisStep.textContent = 'Preparing image for botanical vision analysis...';

    const steps = [
      'Inspecting complete image for distinguishable plants...',
      'Analyzing leaves, flowers, and stems with Google Gemini...',
      'Cross-referencing botanical names with Ayurvedic catalog...',
      'Retrieving traditional health insights and precautions...'
    ];
    let stepIndex = 0;
    if (statusInterval) clearInterval(statusInterval);
    statusInterval = setInterval(() => {
      stepIndex = (stepIndex + 1) % steps.length;
      analysisStep.textContent = steps[stepIndex];
    }, 1200);
  }

  function hideAnalyzingOverlay() {
    if (statusInterval) clearInterval(statusInterval);
    overlay.classList.remove('is-visible');
    overlay.setAttribute('aria-hidden', 'true');
    analyseButton.disabled = false;
  }

  function showAnalysisError(errorMessage) {
    if (statusInterval) clearInterval(statusInterval);
    modalLoader.hidden = true;
    modalProgress.hidden = true;
    analysisTitle.textContent = 'Identification Paused';
    analysisStep.textContent = errorMessage;
    modalErrorActions.hidden = false;
    error.textContent = errorMessage;
  }

  modalDismissButton.addEventListener('click', hideAnalyzingOverlay);
  modalRetryButton.addEventListener('click', triggerAnalysis);

  async function triggerAnalysis() {
    if (!savedImage) return;

    showAnalyzingOverlay();

    try {
      // Prepare FormData
      const formData = new FormData();

      if (activeFileBlob) {
        formData.append('image', activeFileBlob, 'plant_photo.jpg');
      } else {
        // Convert base64 dataUrl to blob
        const res = await fetch(savedImage);
        const blob = await res.blob();
        formData.append('image', blob, 'plant_photo.jpg');
      }

      // Send to FastAPI /api/identify
      const endpoint = `${API_BASE}/api/identify`;
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        let errorDetail = 'Could not analyze plants. Please try again.';
        try {
          const errJson = await response.json();
          if (errJson && errJson.detail) {
            errorDetail = errJson.detail;
          }
        } catch (_) {}

        if (response.status === 429) {
          errorDetail = 'Too many requests right now. Please try again in a moment.';
        } else if (response.status === 503) {
          errorDetail = errorDetail || 'AI vision service is not yet configured with an API key.';
        }

        throw new Error(errorDetail);
      }

      const identificationData = await response.json();

      // Store results in sessionStorage
      try {
        sessionStorage.setItem('ayurscanScanImage', savedImage);
        sessionStorage.setItem('ayurscanScanResults', JSON.stringify(identificationData));
      } catch (storageErr) {
        console.warn('SessionStorage quota warning:', storageErr);
      }

      // Clean redirect to result.html
      if (statusInterval) clearInterval(statusInterval);
      window.location.href = 'result.html';

    } catch (err) {
      console.error('Plant identification error:', err);
      showAnalysisError(err.message || 'An unexpected error occurred during identification.');
    }
  }

  window.addEventListener('pagehide', stopCamera);
})();
