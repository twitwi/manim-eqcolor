print(r'''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Manim Eqcolor Presentation</title>
        <style>

            /* full size: comment this block and tune the size below for a fixed size */
            html, body, div.cont {
                width: 100%;
                height: 100%;
                padding: 0;
                margin: 0;
                background: #010101;
            }
            
            .cont {
                width: 1280px; /* ignored if the block above is present */
                height: 720px; /* ignored if the block above is present */
                position: relative;
            }
            .cont * { /* all descendants ! */
                object-position: center center; /* e.g.: left top */
                object-fit: contain;
                position: absolute;
                left: 0; top: 0;
                width: 100%; height: 100%;
            }
            .cont>div {
                /*width: 100%;*/
            }
            .hide {
                visibility: hidden;
            }
            .cont>*:not(.show) {
                display: none;
            }
            
            /* controls */
            .controls {
                position: absolute;
                height: 0;
                overflow: visible;
                z-index: 1;
            }
        </style>
    </head>
    <body>

        <!--
SOME COMMANDS FOR GENERATING THE VIDEOS:
pip install webm
webm -i pdftoimage/gif_generated/0-1.gif vids/0-1.mp4
webm -i pdftoimage/gif_generated/1-2.gif vids/1-2.mp4
ffmpeg -i vids/1-2.mp4 -vf reverse vids/2-1.mp4
-->

        <div class="controls">
            <button onclick="step(-1)">«</button>
            <button onclick="step( 1)">»</button>
        </div>
        <div class="cont">
            <!-- METTRE CI-DESSOUS LES SLIDES -->

<!--HERE-->

        </div>
        
        <script>
            nothing = () => {}
            current = -1
            onstep = nothing
            
            function step(s) {
                let backward = s<0
                let slides = Array.from(document.querySelectorAll('.cont>*'))
                if (backward && current === 0) return
                if (!backward && current === slides.length) return
                let prev = current
                {
                    os = onstep
                    onstep = nothing
                    os()
                    current = Math.min(Math.max(0, current+s), slides.length)
                    console.log('CURRENT', current, '(prev ', prev,')')
                }
                let c = current
                let im = slides[c]

                let playVideo = (im) => {
                    im.playbackRate = 2 // speedup of the transition
                    if (backward) {
                        im.playbackRate = 4
                    }
                    /*
                    im.onended = () => {
                    }
                    im.onseeked = () => {
                        slides.forEach((e,i) => e.classList.toggle('current', i==c))
                        im.play()
                    }
                    */
                    im.currentTime = 0
                    im.play()
                    /*
                    onstep = () => {
                        im.onended = im.onseeked = undefined
                        im.pause()
                    }*/
                }

                if (prev === -1) { // init
                    Array.from(document.querySelectorAll('.cont>*')).forEach(v => v.classList.toggle('show', false))
                    im.classList.toggle('show', true)
                    if (im.tagName == 'VIDEO') {
                        im.currentTime = 0
                    }
                    if (im.tagName == 'DIV') {
                        im.children[1].classList.toggle('hide', true)
                        im.children[1].currentTime = 0
                        im.children[0].classList.toggle('hide', false)
                        im.children[0].currentTime = 0
                    }
                    return
                }
                if (backward) {
                    if (prev !== slides.length && slides[prev].tagName == 'VIDEO') {
                        slides[prev].classList.toggle('show', false)
                    }
                    if (prev !== slides.length && slides[prev].tagName == 'DIV') {
                        slides[prev].classList.toggle('show', false)
                    }
                    if (im.tagName == 'VIDEO') {
                        im.classList.toggle('show', true)
                        im.currentTime = 0
                        im.pause()
                        onstep = () => {}
                    }
                    if (im.tagName == 'DIV') {
                        im.children[0].classList.toggle('hide', true)
                        im.children[0].currentTime = 0
                        im.children[1].classList.toggle('hide', false)
                        playVideo(im.children[1])
                        im.classList.toggle('show', true)
                        onstep = () => {}
                    }
                } else { // forward
                    if (slides[prev].tagName == 'VIDEO') {
                        playVideo(slides[prev])
                        onstep = () => {
                            slides[prev].pause()
                            slides[prev].classList.toggle('show', false)
                            if (c!==slides.length) im.classList.toggle('show', true)
                        }
                    }
                    if (slides[prev].tagName == 'DIV') {
                        slides[prev].children[1].classList.toggle('hide', true)
                        slides[prev].children[1].currentTime = 0
                        slides[prev].children[0].classList.toggle('hide', false)
                        playVideo(slides[prev].children[0])
                        onstep = () => {
                            slides[prev].children[0].pause()
                            slides[prev].classList.toggle('show', false)
                            if (c!==slides.length) im.classList.toggle('show', true)
                        }
                    }
                }
/*
                // different slide types
                if (im.tagName == 'IMG') {
                    if (im && im.src) {
                        if (im.src.endsWith('.gif')) {
                            let url = im.src
                            im.src = ''
                            im.onerror = im.onload = () => {
                                im.onerror = im.onload = undefined
                                slides.forEach((e,i) => e.classList.toggle('current', i==c))
                            }
                            setTimeout(() => {im.src = url}, 0)
                        } else {
                            slides.forEach((e,i) => e.classList.toggle('current', i==c))
                        }
                    }
                } else if (im.tagName ==  'DIV') {
                    let target = im.children[dir == 'backward' ? 1 : 0]
                    let nextStep = dir == 'backward' ? -1 : +1
                    console.log(im.tagName, target, nextStep, Array.from(im.children))
                    //Array.from(im.children).forEach(e => e.classList.toggle('show', e==target))
                    Array.from(document.querySelectorAll('.cont>*>video')).forEach(e => e.classList.toggle('show', e==target))
                    playVideoThenStep(target, //nextStep) // for when there are systematic intermediate images
                } else if (im.tagName == 'VIDEO') {
                    if (dir == 'backward') {
                        step(-1)
                        return
                    }
                    playVideoThenStep(im//, 1)
                }
*/
            }
            step(1)

            window.addEventListener('keydown', ev => {
                let use = true
                if (ev.code == 'ArrowRight') {
                    step(1)
                } else if (ev.code == 'ArrowLeft') {
                    step(-1)
                } else {
                    use = false
                }
                if (use) {
                    ev.preventDefault()
                }
            })
        </script>
    </body>
</html>
''')
