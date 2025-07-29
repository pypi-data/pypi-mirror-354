
```python
import jokyt
from yt_dlp import YoutubeDL

url = "https://youtu.be/dEbI9mycW1Q?si=bkARn-GvPnpClLwa"

opts = {
    "http_headers": {
        "Cookie": jokyt.cookies()
    }
}

with YoutubeDL(opts) as ydl:
    ydl.download([url])
```