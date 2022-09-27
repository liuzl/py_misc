```sh
pip install pywhisper -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install yt-dlp -i https://pypi.tuna.tsinghua.edu.cn/simple
yt-dlp -x --audio-format mp3 -o sam.mp3 -- WHoWGNQRXb0
export CUDA_VISIBLE_DEVICES=2 && pywhisper --language en --model base -o out -- sam.mp3
```
