// env
BACKEND_ROOT = window.BACKEND_ROOT;

const canvas_new = document.getElementById("drawCanvas");
const prediction = document.querySelector(".prediction");

function submitDrawing() {
  const imageData = canvas_new.toDataURL("image/png");
  sendToBackend(imageData);
}

async function sendToBackend(imageData) {
  try {
    const response = await fetch(`${BACKEND_ROOT}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: imageData }),
    });

    if (!response.ok) {
      throw new Error("some backend error");
    }

    const data = await response.json();
    // console.log(response);
    // console.log(data);
    console.log(`Predicted Digit: ${data.prediction}`);
    prediction.innerHTML = `${data.prediction}`;
  } catch (error) {
    console.log(error);
  }
}

// predict button
const predict_btn = document.querySelector(".predict-button");

predict_btn.addEventListener("click", submitDrawing);
