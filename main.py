from pathlib import Path
import re, html, base64

FONT_PATH = r"dc027189e0ba4cd.woff2"
TEXT_PATH = r"novel_output.txt"
OUT_HTML  = r"novel_render.html"

raw_bytes = Path(TEXT_PATH).read_bytes()

try:
    s = raw_bytes.decode("utf-8")
except UnicodeDecodeError:
    s = raw_bytes.decode("latin-1")

s = s.strip()

if s.startswith("(") and s.endswith(")"):
    body, _ = s[1:-1].rsplit(",", 1)
    body = body.strip()

    if (body.startswith("'") and body.endswith("'")) or (body.startswith('"') and body.endswith('"')):
        body = body[1:-1]

    s = body
    s = re.sub(r'(\r?\n)+\s*\.\.\.[\s\S]*$', '', s)



s = re.sub(r'\\\\u([0-9a-fA-F]{4})', r'\\u\1', s)

s = re.sub(
    r'\\u([0-9a-fA-F]{4})',
    lambda m: chr(int(m.group(1), 16)),
    s
)

s = html.unescape(s)

font_b64 = base64.b64encode(Path(FONT_PATH).read_bytes()).decode("ascii")

page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Novel Render</title>
<style>
@font-face {{
  font-family: 'PUANovel';
  src: url(data:font/woff2;base64,{font_b64}) format('woff2');
}}
html,body{{margin:0;padding:0;background:#fbfbfc;color:#111}}
.reader{{max-width:760px;margin:40px auto;padding:0 20px 60px;
  font-family:'PUANovel','Noto Serif SC','PingFang SC','Microsoft YaHei',serif;
  font-size:18px;line-height:1.85}}
.reader p{{margin:0 0 1em;text-indent:2em}}
.uid{{margin-top:2em;color:#666;font-size:14px}}
</style>
</head>
<body>
  <div class="reader">
{s}
  </div>
</body>
</html>"""

Path(OUT_HTML).write_text(page, encoding="utf-8")
print("HTML written to:", OUT_HTML)
