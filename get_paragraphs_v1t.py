import re

def get_vn_paragraphs(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paras = content.split('\n\n')
    for p in paras:
        if re.search(r'[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]', p.lower()):
            print("=====")
            print(p.strip())

get_vn_paragraphs('_posts/ctf-writeups/2026-06-30-v1t-ctf-2026.md')
