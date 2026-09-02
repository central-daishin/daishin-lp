import anthropic
import json
import datetime
from pathlib import Path

client = anthropic.Anthropic()

TOPICS = [
    "訪問マッサージが在宅リハビリに効果的な理由",
    "医療保険で受けられる訪問はりきゅうとは",
    "退院後の回復を早める在宅リハビリのポイント",
    "要介護認定を受けた方への訪問マッサージ活用法",
    "訪問鍼灸で改善できる症状・お悩みについて",
    "ケアマネージャーと連携した在宅療養のすすめ",
    "訪問マッサージの初回体験の流れと注意点",
    "難病患者様への訪問鍼灸・マッサージの取り組み",
    "拘縮予防に訪問マッサージが大切な理由",
    "訪問施術と介護保険サービスの上手な組み合わせ方",
    "在宅での終末期ケアと訪問鍼灸マッサージ",
    "パーキンソン病と訪問はりきゅうマッサージ",
]

posts_file = Path("posts.json")
data = json.loads(posts_file.read_text(encoding="utf-8"))

today = datetime.date.today()
id_str = today.strftime("%Y-%m-%d")

if any(p["id"] == id_str for p in data["posts"]):
    print("今週の記事は既に存在します。スキップします。")
    exit(0)

week_num = today.isocalendar()[1]
topic = TOPICS[week_num % len(TOPICS)]
date_str = f"{today.year}年{today.month}月{today.day}日"

print(f"記事を生成中: {topic}")

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1500,
    messages=[
        {
            "role": "user",
            "content": f"""鹿児島市の訪問鍼灸マッサージ専門院「セントラル治療院 はりきゅう大心」のブログ記事を書いてください。

テーマ：{topic}

要件：
- 読者は要介護・難病の方のご家族やケアマネージャー
- 300〜400文字程度
- 親しみやすく、専門的すぎない表現
- 最後に「お気軽にご相談ください」などのCTAを含める
- JSONのみ返してください（説明文・コードブロック不要）

出力形式：
{{"title":"記事タイトル","summary":"2文程度の要約","content":"本文（<p>タグで段落区切り）","category":"カテゴリ名"}}"""
        }
    ]
)

response_text = message.content[0].text.strip()
if response_text.startswith("```"):
    lines = response_text.split("\n")
    response_text = "\n".join(lines[1:-1])

article = json.loads(response_text.strip())

new_post = {
    "id": id_str,
    "date": date_str,
    "title": article["title"],
    "summary": article["summary"],
    "content": article["content"],
    "category": article.get("category", "訪問ケア")
}

data["posts"].insert(0, new_post)
data["posts"] = data["posts"][:20]

posts_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"記事を生成しました: {new_post['title']}")
