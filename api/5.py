from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>

    <button id="startRecord">开始录音</button>
    <button id="stopRecord" disabled>停止录音</button>
    <audio id="audio" controls></audio>

    <script type="text/javascript">
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      console.log('getUserMedia supported.');
      let chunks = [];
      let recorder = null;

      const startButton = document.getElementById('startRecord');
      const stopButton = document.getElementById('stopRecord');
      const audioElem = document.getElementById('audio');

      startButton.onclick = function() {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
          recorder = new MediaRecorder(stream);

          recorder.ondataavailable = function(e) {
            chunks.push(e.data);
          }

          recorder.onstop = function() {
            const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
            chunks = [];
            const audioURL = window.URL.createObjectURL(blob);
            audioElem.src = audioURL;

            // 新增的代码：自动播放
            audioElem.play().catch((e) => {
                console.error('自动播放失败:', e);
            });
          }

          recorder.start();
          console.log(recorder.state + "ing...");
          startButton.disabled = true;
          stopButton.disabled = false;
        })
        .catch(function(err) {
          console.log('The following error occurred: ' + err);
        })
      }

      stopButton.onclick = function() {
        recorder.stop();
        console.log(recorder.state);
        startButton.disabled = false;
        stopButton.disabled = true;
      }
    } else {
      console.log('getUserMedia not supported on your browser!');
    }
    </script>

    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)