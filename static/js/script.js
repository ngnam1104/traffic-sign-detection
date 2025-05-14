document.addEventListener("DOMContentLoaded", function () {
  const imageTab = document.getElementById("image-tab");
  const videoTab = document.getElementById("video-tab");
  const cameraTab = document.getElementById("camera-tab");

  const imageSection = document.getElementById("image-section");
  const videoSection = document.getElementById("video-section");
  const cameraSection = document.getElementById("camera-section");

  const imageInput = document.getElementById("image-input");
  const imageSubmitBtn = document.getElementById("image-submit");
  const outputImage = document.getElementById("output-image");
  const imageLoading = document.getElementById("image-loading");
  const imageError = document.getElementById("image-error");

  const videoInput = document.getElementById("video-input");
  const videoSubmitBtn = document.getElementById("video-submit");
  const outputVideo = document.getElementById("output-video");
  const videoLoading = document.getElementById("video-loading");
  const videoError = document.getElementById("video-error");

  const cameraButton = document.getElementById("camera-button");
  const cameraPreview = document.getElementById("camera-preview");
  const cameraCanvas = document.getElementById("camera-canvas");
  const cameraOutput = document.getElementById("camera-output");
  const cameraLoading = document.getElementById("camera-loading");
  const cameraError = document.getElementById("camera-error");

  let cameraStream = null;
  let cameraInterval = null;

  function showLoading(element) {
    element.classList.add("active");
  }

  function hideLoading(element) {
    element.classList.remove("active");
  }

  function showError(element, message) {
    element.textContent = message;
    element.style.display = "block";
  }

  function hideError(element) {
    element.textContent = "";
    element.style.display = "none";
  }

  function disableButton(button) {
    button.disabled = true;
  }

  function enableButton(button) {
    button.disabled = false;
  }

  const tabs = {
    "image-tab": "image-section",
    "video-tab": "video-section",
    "camera-tab": "camera-section",
  };

  Object.keys(tabs).forEach((tabId) => {
    document.getElementById(tabId).addEventListener("click", function (e) {
      e.preventDefault();

      if (cameraStream) {
        clearInterval(cameraInterval);
        cameraInterval = null;
        const tracks = cameraStream.getTracks();
        tracks.forEach((track) => track.stop());
        cameraPreview.srcObject = null;
        cameraStream = null;
        cameraButton.textContent = "Bắt đầu Camera";
        hideLoading(cameraLoading);
        hideError(cameraError);
        enableButton(cameraButton);
      }

      Object.values(tabs).forEach((sectionId) => {
        document.getElementById(sectionId).classList.add("d-none");
      });

      Object.keys(tabs).forEach((id) => {
        document.getElementById(id).classList.remove("selected");
        document.getElementById(id).removeAttribute("aria-current");
      });

      document.getElementById(tabs[tabId]).classList.remove("d-none");
      this.classList.add("selected");
      this.setAttribute("aria-current", "page");

      imageInput.value = null;
      outputImage.src = "/placeholder.svg?height=300&width=400";
      hideLoading(imageLoading);
      hideError(imageError);
      enableButton(imageSubmitBtn);

      videoInput.value = null;
      outputVideo.src = "";
      outputVideo.load();
      hideLoading(videoLoading);
      hideError(videoError);
      enableButton(videoSubmitBtn);

      cameraOutput.src = "/placeholder.svg?height=300&width=400";
    });
  });

  imageInput.addEventListener("change", function (e) {
    if (e.target.files && e.target.files[0]) {
      const reader = new FileReader();
      reader.onload = function (e) {
        outputImage.src = e.target.result;
      };
      reader.readAsDataURL(e.target.files[0]);
      hideError(imageError);
    }
  });

  imageSubmitBtn.addEventListener("click", async function () {
    if (imageSubmitBtn.disabled) return;

    const file = imageInput.files[0];

    if (!file) {
      alert("Vui lòng chọn một file ảnh.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    disableButton(imageSubmitBtn);
    showLoading(imageLoading);
    hideError(imageError);
    outputImage.src = "/placeholder.svg?height=300&width=400";

    try {
      const response = await fetch("/predict_image", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      outputImage.src = result.output_path + "?" + new Date().getTime();
    } catch (error) {
      console.error("Lỗi xử lý ảnh:", error);
      showError(imageError, `Lỗi: ${error.message}`);
      outputImage.src = "/placeholder.svg?height=300&width=400";
    } finally {
      enableButton(imageSubmitBtn);
      hideLoading(imageLoading);
    }
  });

  videoInput.addEventListener("change", function (e) {
    if (e.target.files && e.target.files[0]) {
      outputVideo.src = URL.createObjectURL(e.target.files[0]);
      hideError(videoError);
    }
  });

  videoSubmitBtn.addEventListener("click", async function () {
    const file = videoInput.files[0];

    if (!file) {
      alert("Vui lòng chọn một file video.");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    disableButton(videoSubmitBtn);
    showLoading(videoLoading);
    hideError(videoError);
    outputVideo.src = "";
    outputVideo.load();

    try {
      const response = await fetch("/predict_video", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      const videoSrc = result.output_path + "?" + new Date().getTime();
      outputVideo.src = videoSrc;
      outputVideo.load();
      outputVideo.play();
    } catch (error) {
      console.error("Lỗi xử lý video:", error);
      outputVideo.src = "";
      outputVideo.load();
    } finally {
      enableButton(videoSubmitBtn);
      hideLoading(videoLoading);
    }
  });

  cameraButton.addEventListener("click", async function () {
    hideError(cameraError);

    if (cameraStream) {
      clearInterval(cameraInterval);
      cameraInterval = null;
      const tracks = cameraStream.getTracks();
      tracks.forEach((track) => track.stop());
      cameraPreview.srcObject = null;
      cameraStream = null;
      cameraButton.textContent = "Bắt đầu Camera";
      enableButton(cameraButton);
      hideLoading(cameraLoading);
      cameraOutput.src = "/placeholder.svg?height=300&width=400";
      return;
    } else {
      disableButton(cameraButton);
      showLoading(cameraLoading);
      cameraButton.textContent = "Đang bắt đầu Camera...";
      cameraOutput.src = "/placeholder.svg?height=300&width=400";

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
          });
          cameraPreview.srcObject = stream;
          cameraStream = stream;
          cameraButton.textContent = "Chụp & Phát hiện";

          cameraPreview.onloadedmetadata = () => {
            enableButton(cameraButton);
            hideLoading(cameraLoading);

            cameraInterval = setInterval(async () => {
              const context = cameraCanvas.getContext("2d");
              cameraCanvas.width = cameraPreview.videoWidth;
              cameraCanvas.height = cameraPreview.videoHeight;
              context.drawImage(
                cameraPreview,
                0,
                0,
                cameraCanvas.width,
                cameraCanvas.height
              );
              cameraCanvas.toBlob(
                async function (blob) {
                  if (!blob) {
                    showError(
                      cameraError,
                      "Không thể chụp khung hình từ camera."
                    );
                    return;
                  }

                  const formData = new FormData();
                  formData.append("frame", blob, "camera_frame.jpg");

                  try {
                    const response = await fetch("/predict_camera", {
                      method: "POST",
                      body: formData,
                    });

                    if (!response.ok) {
                      const errorText = await response.text();
                      throw new Error(
                        `Server error: ${response.status} - ${errorText}`
                      );
                    }

                    const result = await response.json();
                    const detections = result.detections;

                    context.clearRect(
                      0,
                      0,
                      cameraCanvas.width,
                      cameraCanvas.height
                    );

                    context.drawImage(
                      cameraPreview,
                      0,
                      0,
                      cameraCanvas.width,
                      cameraCanvas.height
                    );

                    detections.forEach((detection) => {
                      const [x1, y1, x2, y2] = detection.box;
                      const label = detection.label;
                      const confidence = detection.confidence;

                      context.strokeStyle = "red";
                      context.lineWidth = 2;
                      context.strokeRect(x1, y1, x2 - x1, y2 - y1);

                      context.fillStyle = "red";
                      context.font = "12px Arial";
                      context.fillText(
                        label + " (" + confidence.toFixed(2) + ")",
                        x1,
                        y1 - 5
                      );
                    });

                    cameraOutput.src = cameraCanvas.toDataURL(
                      "image/jpeg",
                      0.95
                    );
                  } catch (error) {
                    console.error("Lỗi xử lý khung hình camera:", error);
                    showError(cameraError, `Lỗi: ${error.message}`);
                    cameraOutput.src = "/placeholder.svg?height=300&width=400";
                  }
                },
                "image/jpeg",
                0.95
              );
            }, 41.67);
          };
        } catch (error) {
          console.error("Lỗi truy cập Camera: ", error);
          showError(
            cameraError,
            `Lỗi: ${error.name} - ${error.message}. Vui lòng kiểm tra quyền truy cập camera.`
          );
          cameraButton.textContent = "Bắt đầu Camera";
          enableButton(cameraButton);
          hideLoading(cameraLoading);
        }
      } else {
        showError(
          cameraError,
          "Trình duyệt của bạn không hỗ trợ truy cập camera."
        );
        cameraButton.textContent = "Bắt đầu Camera";
        enableButton(cameraButton);
        hideLoading(cameraLoading);
      }
    }
  });
});
