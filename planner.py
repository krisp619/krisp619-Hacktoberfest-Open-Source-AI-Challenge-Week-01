#!/usr/bin/env python3
"""
Aaj Kay Lavayche (आज काय लावायचं?)
Offline AI Garden Planner for Solapur, Maharashtra, India.
Designed for the Hacktoberfest 'Touch Grass' challenge:
Read one prompt, get actionable sowing advice, and get out into the dirt.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure UTF-8 output across all operating systems and Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Defaults
DEFAULT_MODEL = "llama3.2:3b"
BASE_DIR = Path(__file__).resolve().parent
PLANTS_FILE = BASE_DIR / "plants.json"
LOG_FILE = BASE_DIR / "garden_log.md"

SOLAPUR_SEASONS = {
    "kharif": (6, 9),    # June - September (Monsoon)
    "rabi": (10, 2),     # October - February (Cool/Winter)
    "summer": (3, 5),    # March - May (Hot & Dry)
}

MONTH_NAMES_MR = [
    "", "जानेवारी (January)", "फेब्रुवारी (February)", "मार्च (March)",
    "एप्रिल (April)", "मे (May)", "जून (June)", "जुलै (July)",
    "ऑगस्ट (August)", "सप्टेंबर (September)", "ऑक्टोबर (October)",
    "नोव्हेंबर (November)", "डिसेंबर (December)"
]


def load_plants(filepath: Path = PLANTS_FILE) -> List[Dict[str, Any]]:
    """Loads plant catalog from JSON file."""
    if not filepath.exists():
        raise FileNotFoundError(f"Plants database not found at: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_plants(
    plants: List[Dict[str, Any]],
    month: int,
    container_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Filter plants by active sowing month and container friendliness.
    Month is 1-indexed (1 = January, 12 = December).
    """
    if not (1 <= month <= 12):
        raise ValueError(f"Month must be between 1 and 12, got {month}")

    filtered = []
    for plant in plants:
        if month in plant.get("sow_months", []):
            if container_only and not plant.get("container_friendly", False):
                continue
            filtered.append(plant)
    return filtered


def log_garden_entry(entry_text: str, log_path: Path = LOG_FILE) -> None:
    """Appends a dated log entry to garden_log.md."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    log_line = f"- **{now_str}** — {entry_text.strip()}\n"

    # Create file with header if it doesn't exist
    if not log_path.exists():
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("# 🌿 Aaj Kay Lavayche - Garden Log\n\n")
            f.write("Your personal offline record of sowed seeds, soil mix, and harvests.\n\n")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_line)


def get_garden_history(log_path: Path = LOG_FILE, limit: int = 10) -> List[str]:
    """Retrieves the last `limit` log entries."""
    if not log_path.exists():
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip().startswith("- **")]
    return lines[-limit:]


def build_prompt(
    filtered_plants: List[Dict[str, Any]],
    target_date: datetime.date,
    lang: str = "mr",
    container_only: bool = False
) -> str:
    """Constructs a hyper-focused prompt for a concise outdoor recommendation."""
    month_name = target_date.strftime("%B")
    month_idx = target_date.month
    mr_month = MONTH_NAMES_MR[month_idx]

    # Summarize plant list for context
    plant_summaries = []
    for p in filtered_plants:
        plant_summaries.append(
            f"- {p['marathi_name']} ({p['english_name']}): "
            f"Harvest in {p['days_to_harvest']}, Sun: {p['sunlight']}, "
            f"Container: {'Yes' if p['container_friendly'] else 'No'}. "
            f"Tip: {p['short_tip']}"
        )
    plant_list_text = "\n".join(plant_summaries)

    space_desc = "Balcony / Pots (Containers only)" if container_only else "Ground Garden / Balcony"

    if lang == "en":
        return f"""You are 'Aaj Kay Lavayche', an expert organic gardening assistant for Solapur, Maharashtra, India.
Today's Date: {target_date.strftime('%d %B %Y')} (Month: {month_name}).
Garden Type: {space_desc}
Solapur Climate Context: Hot semi-arid climate with intense afternoon sun and dry winds.

Available plants for sowing right now:
{plant_list_text}

Provide an actionable, quick response so the gardener can close their screen and start planting outside:
1. Top 3 picks to sow this week with Marathi name in Devanagari followed by English name in brackets.
2. 3 short, bulleted step-by-step sowing steps for today.
3. 1 Solapur climate watering tip.

Keep the tone encouraging, authentic, and concise (under 180 words). No long intros or outros."""

    # Default Marathi prompt
    return f"""तुम्ही 'आज काय लावायचं?' (Aaj Kay Lavayche) चे सोलापूरचे स्थानिक परसबाग सल्लागार आहात.
आजची तारीख: {target_date.strftime('%d %B %Y')} (महिना: {mr_month}).
जागेचा प्रकार: {'कुंडी / बाल्कनी (Container)' if container_only else 'परसबाग / कुंडी'}.
हवामान: सोलापूरचे उष्ण व कोरडे हवामान.

या आठवड्यात लावता येणारी झाडे/भाज्या:
{plant_list_text}

कृपया खालील मुद्द्यांवर अगदी संक्षिप्त आणि थेट उत्तर द्या (जास्त वेळ स्क्रीनवर न थांबता बागेत काम सुरू करता यावे):
1. 🌟 या आठवड्यासाठी सर्वोत्तम ३ शिफारसी (मराठी देवनागरी नाव आणि कंसात इंग्रजी नाव, उदा. मेथी (Fenugreek)).
2. 🌱 आजच बियाणे टोकण्यासाठी ३ सोप्या पायऱ्या (Steps).
3. 💧 सोलापूरच्या हवामानासाठी १ महत्त्वाचा पाणी देण्याचा सल्ला (Watering Tip).

टीप: उत्तर शुद्ध, सोप्या मराठीत द्या. स्क्रीन टाईम कमी ठेवण्यासाठी उत्तर संक्षिप्त (१८० शब्दांच्या आत) ठेवा."""


def query_ollama(
    prompt: str,
    model: str = DEFAULT_MODEL
) -> Optional[str]:
    """Queries local Ollama instance with the prompt."""
    try:
        import ollama
    except ImportError:
        raise RuntimeError("The 'ollama' Python package is not installed. Run: pip install ollama")

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.3}
        )
        return response["message"]["content"]
    except Exception as e:
        err_msg = str(e).lower()
        if "connection" in err_msg or "connect" in err_msg or "111" in err_msg or "refused" in err_msg:
            print("\n⚠️  [Ollama Connection Notice]: Cannot connect to local Ollama service.")
            print("   👉 To start Ollama in your terminal, run:")
            print("      ollama serve")
            print("   👉 And make sure you have the lightweight model downloaded:")
            print(f"      ollama pull {model}\n")
        elif "not found" in err_msg or "model" in err_msg:
            print(f"\n⚠️  [Model Notice]: Model '{model}' was not found in Ollama.")
            print(f"   👉 To download it, run:")
            print(f"      ollama pull {model}\n")
        else:
            print(f"\n⚠️  [Ollama Error]: {e}\n")
        return None


def print_fallback_plan(
    filtered_plants: List[Dict[str, Any]],
    target_date: datetime.date,
    container_only: bool,
    lang: str = "mr"
) -> None:
    """Offline rule-based output when Ollama LLM is not active."""
    month_name = target_date.strftime("%B")
    month_idx = target_date.month

    print("=" * 65)
    if lang == "en":
        print(f"🌿 AAJ KAY LAVAYCHE — Sowing Guide ({target_date.strftime('%d %B %Y')})")
        print(f"📍 Location: Solapur | Filter: {'Containers / Pots' if container_only else 'All Garden Spaces'}")
        print("=" * 65)
        print(f"\n✨ Sowing candidates for {month_name} ({len(filtered_plants)} plants found):\n")
        for i, p in enumerate(filtered_plants[:5], start=1):
            cont = "✅ Container Friendly" if p['container_friendly'] else "🌿 Needs Ground/Big Bed"
            print(f" {i}. {p['marathi_name']} ({p['english_name']})")
            print(f"    • Harvest: {p['days_to_harvest']} | Sunlight: {p['sunlight']}")
            print(f"    • Space: {cont}")
            print(f"    • Solapur Tip: {p['short_tip']}\n")
        print("💡 Quick Sowing Rule: Sow seeds at twice their depth, mist with water, place in morning sun.")
        print("💧 Solapur Watering Tip: Water early in the morning before 8 AM to prevent soil baking.")
    else:
        print(f"🌿 आज काय लावायचं? — सोलापूर परसबाग नियोजन ({target_date.strftime('%d %B %Y')})")
        print(f"📍 ठिकाण: सोलापूर | प्रकार: {'फक्त कुंड्या / बाल्कनी' if container_only else 'सर्व परसबाग'}")
        print("=" * 65)
        print(f"\n✨ {MONTH_NAMES_MR[month_idx]} महिन्यातील लागवडीसाठी उपलब्ध वनस्पती ({len(filtered_plants)} पर्याय):\n")
        for i, p in enumerate(filtered_plants[:5], start=1):
            cont = "✅ कुंडीसाठी योग्य" if p['container_friendly'] else "🌿 वाफ्यासाठी/मोठ्या जागेसाठी योग्य"
            print(f" {i}. {p['marathi_name']} ({p['english_name']})")
            print(f"    • काढणी: {p['days_to_harvest']} | ऊन: {p['sunlight']}")
            print(f"    • जागा: {cont}")
            print(f"    • टिप: {p['short_tip']}\n")
        print("💡 लागवड पद्धत: बिया त्यांच्या आकाराच्या दुप्पट खोल पेरा, हलके पाणी मारा व सकाळच्या कोवळ्या उन्हात ठेवा.")
        print("💧 सोलापूर पाणी सल्ला: बाष्पीभवन रोखण्यासाठी सकाळी ८ च्या आधी पाणी द्या आणि मातीवर पालापाचोळ्याचे आच्छादन करा.")
    print("=" * 65)
    print("🌱 Screen time done! Grab your trowel and touch some soil! 🚜\n")


def parse_arguments() -> argparse.Namespace:
    """CLI Argument Parser."""
    parser = argparse.ArgumentParser(
        prog="planner.py",
        description="Aaj Kay Lavayche (आज काय लावायचं?) - Offline AI Garden Planner for Solapur (Hacktoberfest 'Touch Grass')",
        epilog="Examples:\n"
               "  python planner.py\n"
               "  python planner.py --container\n"
               "  python planner.py --lang en\n"
               "  python planner.py --date 2026-10-15 --container\n"
               "  python planner.py --log \"Sowed methi in 10-inch terracotta pot\"\n"
               "  python planner.py --history\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--date",
        type=str,
        help="Custom date in YYYY-MM-DD format (defaults to today)"
    )
    parser.add_argument(
        "--container",
        action="store_true",
        help="Show only container-friendly plants (ideal for balconies and pots)"
    )
    parser.add_argument(
        "--lang",
        choices=["mr", "en"],
        default="mr",
        help="Language output: 'mr' for Marathi (default), 'en' for English"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Ollama model name (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--log",
        type=str,
        metavar="ENTRY",
        help="Append an outdoor garden activity entry to garden_log.md"
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="View recent garden log entries"
    )
    parser.add_argument(
        "--offline-only",
        action="store_true",
        help="Skip Ollama LLM and directly use local plants.json rule-engine"
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    # Feature 1: Garden Log recording
    if args.log:
        log_garden_entry(args.log)
        print(f"✅ Logged to garden_log.md: \"{args.log}\"")
        print("🌱 Great job getting your hands in the dirt!")
        return

    # Feature 2: Garden History
    if args.history:
        history = get_garden_history()
        print("\n📜 Recent Garden Log Entries (garden_log.md):")
        print("-" * 55)
        if not history:
            print("No entries yet. Add your first log with: python planner.py --log \"Sowed palak in pot\"")
        else:
            for entry in history:
                print(entry)
        print("-" * 55)
        return

    # Feature 3: Determine Date
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"❌ Error: Invalid date format '{args.date}'. Please use YYYY-MM-DD.")
            sys.exit(1)
    else:
        target_date = datetime.date.today()

    # Load & Filter Plants
    try:
        all_plants = load_plants()
    except Exception as e:
        print(f"❌ Error loading plants data: {e}")
        sys.exit(1)

    filtered = filter_plants(all_plants, target_date.month, container_only=args.container)

    if not filtered:
        print(f"No plants matched the criteria for month {target_date.month} (container_only={args.container}).")
        return

    # If --offline-only was explicitly requested, skip Ollama query
    if args.offline_only:
        print_fallback_plan(filtered, target_date, args.container, lang=args.lang)
        return

    # Build AI Prompt and Query Local Ollama
    prompt = build_prompt(filtered, target_date, lang=args.lang, container_only=args.container)
    
    # Visual header
    header_title = "🌿 Aaj Kay Lavayche (आज काय लावायचं?) — Solapur Garden Planner"
    print("\n" + "=" * len(header_title))
    print(header_title)
    print(f"📅 Date: {target_date.strftime('%d %B %Y')} | Filter: {'Containers Only' if args.container else 'All Spaces'} | Model: {args.model}")
    print("=" * len(header_title) + "\n")

    ai_response = query_ollama(prompt, model=args.model)

    if ai_response:
        print(ai_response.strip())
        print("\n" + "-" * 60)
        print("🌿 Screen time done! Close your laptop and go touch grass! 👩‍🌾🚜\n")
    else:
        # Fallback to local rule-based database display
        print("🔄 [Offline Fallback Activated] Displaying filtered plant catalog directly:\n")
        print_fallback_plan(filtered, target_date, args.container, lang=args.lang)


if __name__ == "__main__":
    main()
