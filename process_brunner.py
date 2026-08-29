import re
import os
import shutil
import glob

# 1. Create image directory and move images
img_dir = 'assets/img/ctf/brunner-ctf-2026'
os.makedirs(img_dir, exist_ok=True)

tmp_dir = '_tmp_new_ctf'
for img_file in glob.glob(f"{tmp_dir}/*.png") + glob.glob(f"{tmp_dir}/*.jpg"):
    shutil.copy(img_file, img_dir)

# 2. Process markdown
md_path = f"{tmp_dir}/Writeups BrunnerCTF 2026 3c6b8a8ee38b80b48ac4fd0089fd643d.md"
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the title with our custom intro
content = re.sub(r'^# Writeups BrunnerCTF 2026\s*', '', content)

intro = """Chào mừng các bạn đến với writeup giải **BrunnerCTF 2026**! Theo như thông báo từ ban tổ chức, năm nay giải đấu mở rộng quy mô từ một tiệm bánh nhỏ thành một tập đoàn kỳ lân với chủ đề *"Brunnerne goes corporate"*. 

Giải đấu mang đến những thử thách vô cùng thú vị và "ngon miệng" cho tất cả mọi người, từ những "thực tập sinh CTF" mới vào nghề cho đến các "phó chủ tịch điều hành cấp cao". Dưới đây là phần tóm tắt và lời giải chi tiết cho các thử thách mà mình đã giải quyết được. Cùng xem nhé!

"""

# Ensure all level 1 headings are level 2 (except the title which we removed)
content = re.sub(r'^# (\d+\..*)$', r'## \1', content, flags=re.MULTILINE)

# Replace image paths
content = re.sub(r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg))\)', r'![\1](/assets/img/ctf/brunner-ctf-2026/\2)', content)

# Replace pronouns (Tôi -> Mình)
def replace_toi(match):
    word = match.group(0)
    if word == 'Tôi': return 'Mình'
    elif word == 'TÔI': return 'MÌNH'
    else: return 'mình'
content = re.sub(r'\btôi\b', replace_toi, content, flags=re.IGNORECASE)

# Construct front matter
front_matter = """---
title: "BrunnerCTF 2026 Writeup"
date: 2026-06-29 00:00:00 +0700
categories: [CTF Writeups]
tags: [ctf, brunner-ctf-2026, writeup]
pin: true
image:
  path: /assets/img/ctf/brunner-ctf-2026/image.png
description: "Chào mừng các bạn đến với writeup giải BrunnerCTF 2026! Giải đấu năm nay mang chủ đề 'Brunnerne goes corporate' với rất nhiều thử thách thú vị..."
---

"""

# Hide the banner on the post page
style_tag = '\n<style>\n  .page-cover, .post-image, .preview-img, img[src*="image.png"]:first-of-type { display: none !important; }\n</style>\n'

final_content = front_matter + intro + content + style_tag

with open('_posts/ctf-writeups/2026-06-29-brunner-ctf-2026.md', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Done processing BrunnerCTF 2026")
