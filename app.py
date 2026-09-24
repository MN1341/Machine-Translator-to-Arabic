import os
import sys
import argparse
from utils.translator import EnglishToArabicTranslator
from utils.visualization import format_cli_banner, calculate_text_metrics

def main():
    parser = argparse.ArgumentParser(description="NLP English-to-Arabic Machine Translation CLI")
    parser.add_argument("--text", "-t", type=str, help="English text sequence to translate")
    parser.add_argument("--file", "-f", type=str, help="Path to text file containing English content")
    parser.add_argument("--beams", "-b", type=int, default=4, help="Beam search decoding size (default: 4)")
    args = parser.parse_args()

    print(format_cli_banner("NLP English -> Arabic Machine Translation CLI"))
    
    config_path = os.path.join(os.path.dirname(__file__), "model", "config.json")
    translator = EnglishToArabicTranslator(config_path=config_path)

    # If text is provided via command line argument
    if args.text:
        input_text = args.text
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: Specified input file '{args.file}' does not exist.")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            input_text = f.read()
    else:
        # Interactive Mode
        print("💡 Interactive Translation Mode (Type 'exit' or 'q' to quit)")
        print("-" * 65)
        while True:
            try:
                user_input = input("\nEnter English text: ").strip()
                if user_input.lower() in ["exit", "q", "quit"]:
                    print("\nExiting Translator CLI. Goodbye!")
                    break
                if not user_input:
                    continue

                print("\n[Translating...]")
                arabic_translation = translator.translate(user_input, num_beams=args.beams)
                metrics = calculate_text_metrics(user_input, arabic_translation)
                
                print("-" * 65)
                print(f"🇬🇧 Input (EN): {user_input}")
                print(f"🇸🇦 Output (AR): {arabic_translation}")
                print("-" * 65)
                print(f"📊 Stats: {metrics['en_word_count']} words (EN) -> {metrics['ar_word_count']} words (AR) | Reading Time: ~{metrics['reading_time_sec']}s")
            except KeyboardInterrupt:
                print("\nExiting Translator CLI.")
                break
        return

    # Process single input from CLI argument or file
    print(f"\n[Processing input using MarianMT (Beams: {args.beams})...]")
    arabic_translation = translator.translate(input_text, num_beams=args.beams)
    metrics = calculate_text_metrics(input_text, arabic_translation)
    
    print("-" * 65)
    print("🇬🇧 English Input:")
    print(input_text)
    print("\n🇸🇦 Arabic Translation:")
    print(arabic_translation)
    print("-" * 65)
    print(f"📊 Metrics: {metrics['en_word_count']} EN words | {metrics['ar_word_count']} AR words | Est. Reading Time: {metrics['reading_time_sec']}s")

if __name__ == "__main__":
    main()
