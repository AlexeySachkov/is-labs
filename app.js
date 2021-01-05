const inputCanvas = $('.inputCanvas')
const scaledInputCanvas = $('.scaledInput')
const outputLabel = $('.outputLabel')

const nn = new NeuralNetwork(784, 128, 64, 32, 10)
nn.setWeights(trainedWeights.map(weight => math.matrix(weight)))
let inputPixels = new Array(784).fill(0)

let mousePressed = false
let lastX = 0
let lastY = 0

const draw = function(x, y) {
  if (mousePressed) {
    const ctx = inputCanvas[0].getContext('2d')
    ctx.beginPath()
    ctx.strokeStyle = 'white'
    ctx.lineWidth = 8
    ctx.lineJoin = 'round'
    ctx.moveTo(lastX, lastY)
    ctx.lineTo(x, y)
    ctx.closePath()
    ctx.stroke()
  }

  lastX = x
  lastY = y

  setTimeout(scaleTo28x28, 0)
}

const scaleTo28x28 = function() {
  inputPixels = []
  const ctx = inputCanvas[0].getContext('2d')
  const scaledctx = scaledInputCanvas[0].getContext('2d')
  const scaledImageData = scaledctx.createImageData(28, 28)

  const downsampleInputForPoint = (x, y) => {
    const input = ctx.getImageData(x * 8, y * 8, 8, 8)
    return input.data.reduce((sum, value, index) => {
      sum[index % 4] += value
      return sum;
    }, [0, 0, 0, 0]).map((sum) => Math.floor(sum / 64))
  }

  for (let row = 0; row < 28; row++) {
    for (let col = 0; col < 28; col++) {
      const index = (row * 28 * 4) + col * 4
      const rgbScaled = downsampleInputForPoint(col, row)
      const grayscale = (rgbScaled[0] + rgbScaled[1] + rgbScaled[2]) / (3 * 255)
      inputPixels.push(grayscale)
      scaledImageData.data[index] = grayscale * 255
      scaledImageData.data[index + 1] = grayscale * 255
      scaledImageData.data[index + 2] = grayscale * 255
      scaledImageData.data[index + 3] = rgbScaled[3] //alpha
    }
  }

  scaledctx.putImageData(scaledImageData, 0, 0)
}

const clearCanvas = function() {
  const ctx = inputCanvas[0].getContext('2d')
  ctx.fillStyle = '#000000'
  ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height)
}

const registerEvents = function() {
  inputCanvas.mousedown(function(e) {
    mousePressed = true
  });

  inputCanvas.mouseup(function(e) {
    mousePressed = false
  });

  inputCanvas.mouseleave(function(e) {
    mousePressed = false
  });

  inputCanvas.mousemove(function(e) {
    draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top)
  })

  $('.clearButton').click(function(e) {
    clearCanvas()
    outputLabel.text('-')
    setTimeout(scaleTo28x28(), 0)
  })

  $('.predictButton').click(function(e) {
    let output = nn.predict(math.matrix(inputPixels))._data
    let prediction = 0;

    let highest = 0
    for (let i = 0; i < output.length; i++) {
      if (output[i] > highest) {
        prediction = i
        highest = output[i]
      }
    }

    outputLabel.text(prediction)
  })
}

$(document).ready(registerEvents())