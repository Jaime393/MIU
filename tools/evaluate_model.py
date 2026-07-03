import argparse, json, os
from datetime import datetime
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--samples', type=int, default=20)
    p.add_argument('--output', default='results/eval.json')
    a = p.parse_args()
    qs = [
        "What is fractal dimension D_f and how does it measure socioecological inequality?",
        "Why is K_i circular while D_f is falsifiable?",
        "Describe power-law fitting for urban complexity."
    ]
    results = []
    try:
        from huggingface_hub import InferenceClient
        c = InferenceClient(model=a.model, token=os.environ.get('HF_TOKEN'))
        for q in qs[:a.samples]:
            try:
                r = c.text_generation(q, max_new_tokens=200)
                results.append({'ok': True, 'len': len(r)})
            except Exception as e:
                results.append({'ok': False, 'err': str(e)})
    except Exception as e:
        results.append({'err': str(e)})
    score = sum(1 for r in results if r.get("ok")) / max(len(results), 1) * 100
    tier = "ELITE" if score >= 80 else "SOLID" if score >= 60 else "BASELINE" if score >= 40 else "WEAK"
    out = {"model": a.model, "date": datetime.now().isoformat(), "score": round(score, 2), "tier": tier}
    os.makedirs(os.path.dirname(a.output) or ".", exist_ok=True)
    open(a.output, "w").write(json.dumps(out, indent=2))
    print(f"Score: {score:.1f}/100 ({tier})")
if __name__ == '__main__': main()