import re

def get_vn_paragraphs(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # split by double newline
    paras = content.split('\n\n')
    print(f"--- {filename} ---")
    for p in paras:
        # if contains lowercase vietnamese character
        if re.search(r'[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]', p.lower()):
            print("=====")
            print(p.strip())
            print("=====")

get_vn_paragraphs('_posts/ctf-writeups/2026-06-29-brunner-ctf-2026.md')
