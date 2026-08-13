from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
frames_src = [root / "screen.png", root / "docs" / "login.png"]
size = (960, 540)
frames = []
for src in frames_src:
    im = Image.open(src).convert("RGB")
    im = im.resize(size, Image.Resampling.LANCZOS)
    frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=128))

out = root / "docs" / "tour.gif"
out.parent.mkdir(exist_ok=True)
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=2800,
    loop=0,
    optimize=True,
)
print("wrote", out, "bytes", out.stat().st_size)
