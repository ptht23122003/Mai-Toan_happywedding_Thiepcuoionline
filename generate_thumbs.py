"""
Two-tier strategy:
- images/gallery-full/   : ảnh GỐC nguyên bản (cho lightbox xem chi tiết)
- images/gallery/        : ảnh THUMB 800px (cho grid lướt nhanh)
"""
from PIL import Image
import os, shutil, pathlib, time

SRC_DIR  = pathlib.Path("images/gallery")
FULL_DIR = pathlib.Path("images/gallery-full")
THUMB_MAX = 800     # max dimension for thumbnail
THUMB_Q   = 90      # JPEG quality for thumbnail

# Step 1: Backup originals to gallery-full/
print("=== STEP 1: Backup ảnh gốc → images/gallery-full/ ===")
FULL_DIR.mkdir(exist_ok=True)
files = sorted(SRC_DIR.glob("DSC_*.jpg"))
print(f"Tìm thấy {len(files)} ảnh gốc")

for f in files:
    dst = FULL_DIR / f.name
    if not dst.exists():
        shutil.copy2(f, dst)

orig_total = sum(p.stat().st_size for p in FULL_DIR.glob("*.jpg"))
print(f"✓ Đã copy. Tổng dung lượng gốc: {orig_total/1024/1024:.1f} MB\n")

# Step 2: Resize originals → thumbnails in gallery/
print("=== STEP 2: Sinh thumbnail trong images/gallery/ ===")
t0 = time.time()
for i, f in enumerate(files, 1):
    img = Image.open(FULL_DIR / f.name)  # đọc từ backup (chắc chắn là gốc)
    w, h = img.size
    if w > h:
        new_w = min(THUMB_MAX, w); new_h = int(h * new_w / w)
    else:
        new_h = min(THUMB_MAX, h); new_w = int(w * new_h / h)
    img.thumbnail((new_w, new_h), Image.Resampling.LANCZOS)
    img = img.convert("RGB")
    img.save(f, "JPEG", quality=THUMB_Q, optimize=True, progressive=True)
    print(f"  [{i:2}/{len(files)}] {f.name:20}  →  {img.size[0]}x{img.size[1]}  {f.stat().st_size/1024:.0f} KB")

thumb_total = sum(p.stat().st_size for p in SRC_DIR.glob("DSC_*.jpg"))
elapsed = time.time() - t0

print(f"\n✓ Xong sau {elapsed:.1f}s")
print(f"\n=== TỔNG KẾT ===")
print(f"Ảnh gốc:    {orig_total/1024/1024:>7.1f} MB  (40 file ở gallery-full/)")
print(f"Thumbnail:  {thumb_total/1024/1024:>7.1f} MB  (40 file ở gallery/)")
print(f"Giảm:       {(1 - thumb_total/orig_total)*100:.1f}%")
