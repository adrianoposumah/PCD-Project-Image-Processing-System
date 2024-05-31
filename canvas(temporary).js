document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("canvas");
  const canvasArea = document.querySelector(".canvas-area");
  const context = canvas.getContext("2d");
  let draw_color = "black";
  let draw_width = "2";
  let is_drawing = false;
  let restore_array = [];
  let index = -1;
  const start_background_color = "white";

  function resizeCanvas() {
    canvas.width = canvasArea.clientWidth;
    canvas.height = canvasArea.clientHeight;
    context.fillStyle = start_background_color;
    context.fillRect(0, 0, canvas.width, canvas.height);
  }

  function change_color(element) {
    draw_color = element.style.backgroundColor;
  }

  function clear_canvas() {
    context.fillStyle = start_background_color;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillRect(0, 0, canvas.width, canvas.height);
    restore_array = [];
    index = -1;
  }

  function undo_last() {
    if (index <= 0) {
      clear_canvas();
    } else {
      index -= 1;
      restore_array.pop();
      context.putImageData(restore_array[index], 0, 0);
    }
  }

  function setDrawColor(color) {
    draw_color = color;
  }

  function setDrawWidth(width) {
    draw_width = width;
  }

  function start(event) {
    if (document.querySelector(".active-pencil").classList.contains("active")) {
      is_drawing = true;
      context.beginPath();
      context.moveTo(getX(event), getY(event));
      event.preventDefault();
    }
  }

  function draw(event) {
    if (is_drawing && document.querySelector(".active-pencil").classList.contains("active")) {
      context.lineTo(getX(event), getY(event));
      context.strokeStyle = draw_color;
      context.lineWidth = draw_width;
      context.lineCap = "round";
      context.lineJoin = "round";
      context.stroke();
    }
    event.preventDefault();
  }

  function stop(event) {
    if (is_drawing) {
      context.stroke();
      context.closePath();
      is_drawing = false;
    }
    event.preventDefault();

    if (event.type != "mouseout") {
      restore_array.push(context.getImageData(0, 0, canvas.width, canvas.height));
      index += 1;
    }
  }

  function getX(event) {
    if (event.touches && event.touches.length > 0) {
      return event.touches[0].clientX - canvas.offsetLeft;
    } else {
      return event.clientX - canvas.offsetLeft;
    }
  }

  function getY(event) {
    if (event.touches && event.touches.length > 0) {
      return event.touches[0].clientY - canvas.offsetTop;
    } else {
      return event.clientY - canvas.offsetTop;
    }
  }

  canvas.addEventListener("touchstart", start, false);
  canvas.addEventListener("touchmove", draw, false);
  canvas.addEventListener("touchend", stop, false);
  canvas.addEventListener("mousedown", start, false);
  canvas.addEventListener("mousemove", draw, false);
  canvas.addEventListener("mouseup", stop, false);
  canvas.addEventListener("mouseout", stop, false);

  // Set canvas size and fill on load
  resizeCanvas();

  // Optionally, resize canvas and fill on window resize
  window.addEventListener("resize", resizeCanvas);

  // Make functions global
  window.change_color = change_color;
  window.clear_canvas = clear_canvas;
  window.undo_last = undo_last;
  window.setDrawColor = setDrawColor;
  window.setDrawWidth = setDrawWidth;
});
