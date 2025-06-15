const canvas = document.getElementById("drawCanvas");
const ctx = canvas.getContext("2d");
let isDrawing = false;

// set canvas background to white
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

// mouse event handlers
canvas.addEventListener("mousedown", (e) => {
  isDrawing = true;
  ctx.beginPath(); // start new stroke
  draw(e);
});

canvas.addEventListener("mousemove", draw);

canvas.addEventListener("mouseup", () => {
  isDrawing = false;
});

canvas.addEventListener("mouseout", () => {
  isDrawing = false;
});

function draw(e) {
  if (!isDrawing) return;

  ctx.lineWidth = 15;
  ctx.lineCap = "round";
  ctx.strokeStyle = "black";

  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath(); // prevent auto-connect
  ctx.moveTo(x, y); // start new segment
}

function clearCanvas() {
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
}

// reset button
document.querySelector(".reset-button").addEventListener("click", clearCanvas);
