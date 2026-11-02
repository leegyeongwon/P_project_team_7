import os
import re
import json

# ===================== 설정 =====================
folder_path = "."                  # TXT 파일들이 있는 폴더
output_folder = "./전처리_결과"
os.makedirs(output_folder, exist_ok=True)

# 작품 정보 (파일명 기준으로 매핑)
work_info = {
    "01_봄봄_김유정": {"title": "봄봄", "author": "김유정"},
    "02_운수좋은날_현진건": {"title": "운수 좋은 날", "author": "현진건"},
    "03_메밀꽃필무렵_이효석": {"title": "메밀꽃 필 무렵", "author": "이효석"},
    "04_날개_이상": {"title": "날개", "author": "이상"},
    "05_치숙_채만식": {"title": "치숙", "author": "채만식"},
}

# ===================== 함수 =====================
def clean_text(text):
    """계획서 기준 정제: 목차·머리말 등 제거, 문장부호·대화 유지"""
    # 흔한 목차/머리말 패턴 제거 (필요시 추가)
    text = re.sub(r'(목차|차례|Contents).*?\n\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(머리말|서문|저자 소개).*?\n\n', '', text, flags=re.IGNORECASE)
    
    # 연속 공백·줄바꿈 정리
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_style_features(text):
    """문체 특징 추출 (계획서 4.1 참고)"""
    sentences = re.split(r'[.!?]\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    avg_sent_len = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
    dialogue_ratio = len(re.findall(r'[“”"「」]', text)) / max(len(text), 1)
    
    words = re.findall(r'[가-힣]+', text)
    vocab_diversity = len(set(words)) / max(len(words), 1)
    
    return {
        "avg_sentence_length": round(avg_sent_len, 2),
        "dialogue_ratio": round(dialogue_ratio, 4),
        "vocab_diversity": round(vocab_diversity, 4),
        "char_count": len(text)
    }

def split_into_chunks(text, max_length=800):
    """문단 경계 우선으로 청크 분할 (사건 순서 유지)"""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    current = ""
    
    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_length:
            current += p + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            current = p + "\n\n"
    
    if current:
        chunks.append(current.strip())
    return chunks

# ===================== 메인 처리 =====================
all_metadata = []

files = [f for f in os.listdir(folder_path) if f.endswith('.txt') and not f.startswith('전처리')]

for filename in sorted(files):
    base_name = filename.replace('.txt', '')
    info = work_info.get(base_name, {"title": base_name, "author": "미상"})
    
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    cleaned = clean_text(raw_text)
    chunks = split_into_chunks(cleaned, max_length=800)
    
    for i, chunk in enumerate(chunks, 1):
        features = extract_style_features(chunk)
        
        # 청크 파일 저장
        chunk_filename = f"{base_name}_chunk{i:03d}.txt"
        chunk_path = os.path.join(output_folder, chunk_filename)
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
        
        # 메타데이터 기록
        meta = {
            "work_id": base_name,
            "title": info["title"],
            "author": info["author"],
            "chunk_id": i,
            "chunk_file": chunk_filename,
            "char_start": None,   # 필요시 나중에 계산 가능
            "style_features": features,
            "source": "공유마당"
        }
        all_metadata.append(meta)
    
    print(f"{filename} → {len(chunks)}개 청크 생성")

# 전체 메타데이터 JSON 저장
meta_path = os.path.join(output_folder, "metadata.json")
with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(all_metadata, f, ensure_ascii=False, indent=2)

print(f"\n전처리 완료! 총 {len(all_metadata)}개 청크")
print(f"결과 폴더: {output_folder}")
print(f"메타데이터: {meta_path}")



