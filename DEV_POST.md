---
title: "Aaj Kay Lavayche: An Offline Local-AI Garden Planner That Told Me to Shut My Laptop and Touch Soil"
published: false
description: "How I built an offline garden planner for Solapur with Python, Ollama, and Llama 3.2 to get gardeners off their screens and into the outdoors."
tags: "devchallenge, hacktoberfest, opensource, ai"
cover_image: ""
---

*This article is a submission for the Hacktoberfest Open-Source AI Challenge: Touch Grass.*

---

## 🌾 What I Built

Living in **Solapur, Maharashtra (India)** — a region known for its intense sun, semi-arid climate, and rich black soil — I often find myself wanting to grow fresh vegetables on my terrace and balcony. But whenever I looked for gardening advice online, I found myself falling into a familiar trap: opening social media, watching 15-minute clickbait videos, and getting lost in sprawling garden forums. 

Instead of getting my hands into the dirt, I was just staring at another screen.

To fix this, I built **"Aaj Kay Lavayche" (Marathi: *आज काय लावायचं?* / *"What should I sow today?"*)** — an offline-first, local-AI garden planner. 

It runs on a single terminal command:
```bash
python planner.py --container
```
In less than five seconds, a local, open-weight language model filters a localized botanical database, evaluates today's date and seasonal conditions, and outputs:
1. **Top 3 plants to sow this week** in simple, native Marathi (Devanagari) with English names in brackets.
2. **Three step-by-step planting instructions**.
3. **One practical watering tip** tailored to Solapur’s dry climate.
4. An immediate closing prompt: *"Screen time done! Close your laptop and go touch grass!"*

No infinite scroll, no push notifications, no cloud signups. Just one actionable recommendation, and you're outside.

---

## 📺 Demo

Here is the exact output running offline on my machine with `llama3.2:3b`:

```text
=============================================================
🌿 Aaj Kay Lavayche (आज काय लावायचं?) — Solapur Garden Planner
📅 Date: 09 October 2026 | Filter: Containers Only | Model: llama3.2:3b
=============================================================

🌟 आठवड्यासाठी सर्वोत्तम ३ शिफारसी:

1. मेथी (Fenugreek) - ऑक्टोबरच्या हवेत उथळ कुंडीतही २५-३० दिवसांत भरघोस उगवते.
2. पालक (Spinach) - रब्बी हंगामात पालकाची वाढ जोमाने होते. पानांची छाटणी केल्यास ३-४ वेळा ताजी पाने मिळतात.
3. तुळस (Holy Basil) - कुंडीत सहज वाढते. वरच्या मंजिऱ्या खुडल्यास झाड दाट होते.

🌱 आजच बियाणे टोकण्यासाठी ३ सोप्या पायऱ्या:
1. माती आणि गांडूळ खत (१:१) मिश्रण कुंडीत भरा.
2. बियाणे हलक्या हाताने १/२ इंच खोल पेरा.
3. झारीने हलके पाणी शिंपडा आणि सकाळच्या कोवळ्या उन्हात ठेवा.

💧 सोलापूरच्या हवामानासाठी १ महत्त्वाचा पाणी देण्याचा सल्ला:
- सोलापूरच्या कोरड्या हवेत माती लवकर कडक होते; बाष्पीभवन रोखण्यासाठी सकाळी ८ च्या आधी पाणी द्या.

------------------------------------------------------------
🌿 Screen time done! Close your laptop and go touch grass! 👩‍🌾🚜
```

You can also record outdoor garden logs directly from your command line:
```bash
python planner.py --log "Sowed methi and palak in 10-inch terracotta pots"
```

---

## 💻 Code

The entire project is open-source under the MIT License on GitHub:

🔗 **GitHub Repository:** [https://github.com/your-username/aaj-kay-lavayche](https://github.com/your-username/aaj-kay-lavayche) *(replace with your GitHub repository link)*

---

## 🛠️ How I Built It

I wanted this tool to be as minimal, lightweight, and resilient as possible:
- **Language & Runtime:** Python 3.10+ with standard libraries (`json`, `argparse`, `datetime`, `pathlib`).
- **Data Layer (`plants.json`):** A curated catalog of 20 native crop varieties suited to Solapur's three core agro-climatic seasons (Kharif, Rabi, Summer), detailing sunlight requirements, days to harvest, container feasibility, and hyper-local tips.
- **Local AI Engine:** [Ollama](https://ollama.com) driving `llama3.2:3b` (a 3-billion parameter model that easily runs on an 8GB RAM laptop with zero GPU acceleration required).
- **Offline Fallback Architecture:** If Ollama isn't running or your device is on low-power mode, the tool automatically falls back to an offline rule engine so you are never left hanging without a plan.
- **Testing:** Comprehensive `pytest` test suite verifying seasonal month logic and container space constraints.

---

## 🔓 Why Open-Source AI Mattered

This project wouldn't make sense with a proprietary cloud API like OpenAI or Claude. Here is why local, open-source AI was essential:

1. **Terraces and gardens have terrible Wi-Fi:** When I take my laptop or device out to my terrace or backyard corner, internet connectivity drops. Local AI runs 100% offline.
2. **Zero Cloud Bills & Zero Rate Limits:** Gardeners shouldn't need an API credit balance or a subscription fee just to plant spinach.
3. **Hyper-Local Customization:** Open weights and open data allow anyone to fork the project, change `plants.json` to their own district (Pune, Nashik, or another continent), and test different models (Qwen, Gemma, Llama).
4. **Privacy:** My personal garden journal and sowing logs live in plain markdown (`garden_log.md`) on my own storage drive.

---

## 🌿 Taking It Outside (My Real Experience)

<!-- Place your personal notes and photos below -->
After generating my plan for October (the start of Maharashtra's Rabi season), the CLI picked **Methi (Fenugreek)** and **Palak (Spinach)**.

I immediately shut the lid of my laptop, grabbed an old 10-inch terracotta pot, mixed red garden soil with vermicompost and coco-peat, and sowed the fenugreek seeds. Spending 45 minutes with my hands in cool soil while the evening breeze picked up was ten times more refreshing than reading another gardening blog.

```markdown
<!-- Upload your outdoor gardening photos here -->
![Testing Aaj Kay Lavayche Outdoors](https://your-image-url-here.jpg)
```

---

## 🚀 What's Next

- 🌦️ Adding a local sensor interface (reading soil moisture sensors via Arduino/Raspberry Pi over serial).
- 🐛 Offline pest diagnostic guides in Marathi for common Solapur vegetable diseases.
- 🤝 Community-contributed regional presets for other drought-prone districts across Maharashtra.

---

*Grab some seeds, run the command, and go touch grass!* 🌿👩‍🌾
