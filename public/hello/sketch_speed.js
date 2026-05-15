let videoPaths = []
let videoDuration = []
let circles = []

let videoPool = []
let videoPoolSize = 9
let RespawnTime = 20000 //задержка перед появление нового круга
let VideoCount = 145 //столько видео в папке

let circleCount = 9
let videoOrder = []
let currentIndex = 0


// p5 вызывает preload() до setup().
// Здесь заранее собираем список путей к видео.
function preload() {
    for (let i = 1; i <= VideoCount; i++) {
        videoPaths.push("/videos/video" + nf(i, 3) + ".mp4")
    }
//заполняю длительностями видео в формате строки, надо потом менять на float
    videoDuration = loadStrings('/hello/videos/Durations.txt');
}

// setup() выполняется один раз при старте.
// Здесь создаётся canvas, пул video-элементов и все круги.
function setup() {
    createCanvas(windowWidth, windowHeight)

    initShuffle()

    // Пул видеоплееров нужен, чтобы не создавать новый <video> для каждого круга.
    for (let i = 0; i < videoPoolSize; i++) {
        let v = createVideo("")
        v.hide()
        v.volume(0)
        v.elt.muted = true
        v.pause()
        videoPool.push(v)
    }

    // Создаём все круги заранее.
    // Каждый круг сам выберет видео при reset().
    for (let i = 0; i < circleCount; i++) {
        circles.push(new ClipCircle())
    }
}

// draw() вызывается каждый кадр.
// Здесь обновляется и рисуется каждый круг.
function draw() {
    background(0)

    for (let c of circles) {
        c.update()
        c.display()
    }
}

function initShuffle(){

    videoOrder = []

    for(let i = 0; i < VideoCount; i++){
        videoOrder.push(i)
    }

    //shuffle(videoOrder, true) // p5.js shuffle
    currentIndex = 0

}

// Класс одного круга с видео внутри.
class ClipCircle {
    constructor() {
        // Сразу запускаем первый цикл жизни круга.
        this.reset(true)
    }

    // reset() переинициализирует круг:
    // - выбирает новое видео
    // - ставит стартовую позицию
    // - рассчитывает скорость по длительности видео
    reset(initial = false) {

        this.index =  getNextVideoIndex() //floor(random(videoPaths.length)) //VideoIndex
        this.visible = true
        this.respawnAt = 0
        //if (VideoIndex > VideoCount - 2) {VideoIndex += 1} else {VideoIndex = 0}

        this.video = getFreeVideo()
        if (!this.video) return

        // Подключаем нужный файл, запускаем с начала.
        this.video.attribute("src", videoPaths[this.index])
        this.video.time(0)
        this.video.play()

        this.size = random(150, 300)
        this.y = random(this.size / 2, height - this.size / 2)

        // Движение слева направо
        this.x = initial ? random(width) : -this.size

        // Длительность видео нужна, чтобы круг прошёл экран за это же время.
        this.duration = float (videoDuration[this.index]) //this.video.duration() || 10
        this.speed = initial ? (width + this.size * 2 - this.x) / (this.duration * 60) : (width + this.size * 3) / (this.duration * 60) //60, почему?

        // Небольшое движение по Y
        this.yDrift = random(-0.15, 0.15)
    }

    // update() отвечает за движение и за жизненный цикл круга.
    update() {
        if (!this.video) return

        if (this.respawnAt > 0) {
            if (millis() >= this.respawnAt) {
                this.respawnAt = 0
                //this.video.attribute("src", "")
                this.reset ()
                return //зачем-то добавил
            }
            return
        }
        // Движение по X
        this.x += this.speed

        // Очень лёгкий дрейф по Y
        this.y += this.yDrift

        if (this.y < this.size / 2) this.y = this.size / 2
        if (this.y > height - this.size / 2) this.y = height - this.size / 2

        // Если видео закончилось, запускаем его снова с начала.
        if (this.video.elt.ended) {
            this.video.time(0)
            this.video.play()
        }

        // Когда круг уходит за правый край, освобождаем видео и создаём новый цикл.
        if (this.x > width + this.size) {
            this.video.pause()
            this.visible = false
            //this.reset()
            this.respawnAt = millis() + random(0, RespawnTime)
            return
        }


    }





    // display() рисует видео внутри круглой маски.
    display() {
        if (!this.video) return

        push()
        drawingContext.beginPath()
        drawingContext.arc(this.x, this.y, this.size / 2, 0, TWO_PI)
        drawingContext.clip()

        imageMode(CENTER)
        image(this.video, this.x, this.y, this.size, this.size)

        pop()
    }
}

// getFreeVideo() ищет свободный video-элемент в пуле.
function getFreeVideo() {
    for (let v of videoPool) {
        if (v.elt.paused || v.elt.ended) {
            return v
        }
    }

    return null
}

//получение индекса видео из перемешанных
function getNextVideoIndex(){

    if(currentIndex >= videoOrder.length){
        initShuffle() // начинаем новый цикл
    }

    let index = videoOrder[currentIndex]
    currentIndex++

    return index

}

// windowResized() вызывается p5 при изменении размеров окна.
function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}