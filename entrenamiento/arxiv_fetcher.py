"""
FETCHER AUTOMÁTICO DE ARXIV — Nodo Darwin Core
===============================================
Busca papers recientes en arXiv sobre:
- Dimensionalidad efectiva / fractales cuánticos
- Coherencia neuronal / resonancia informacional
- Complejidad fractal en sistemas complejos

Los papers absorbidos se convierten automáticamente en huesos MIU.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
from pathlib import Path

class ArxivFetcher:
    """Absorbe papers de arXiv y los convierte en huesos MIU."""

    BASE_URL = "http://export.arxiv.org/api/query"

    QUERIES = [
        ("effective+dimensionality+fractal+quantum", "D_f cuántico"),
        ("neural+coherence+fractal+dimension+brain", "Conectoma fractal"),
        ("informational+resonance+consciousness+field", "Resonancia conciencia"),
        ("complex+systems+fractal+dimension+climate", "Fractal clima"),
        ("Hausdorff+dimension+measurement+quantum+path", "Medición cuántica D_f"),
    ]

    def __init__(self, cache_dir="cache_arxiv"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def search(self, query, max_results=5):
        """Busca papers en arXiv."""
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MIU-DarwinCore/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode()
        except Exception as e:
            print(f"[arXiv] Error buscando '{query}': {e}")
            return None

    def parse_results(self, xml_data):
        """Parsea resultados XML de arXiv."""
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom"
        }
        root = ET.fromstring(xml_data)
        entries = root.findall("atom:entry", ns)

        papers = []
        for entry in entries:
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            arxiv_id = entry.find("atom:id", ns)
            published = entry.find("atom:published", ns)

            paper = {
                "title": title.text.strip() if title is not None else "Sin título",
                "summary": summary.text.strip()[:500] if summary is not None else "",
                "arxiv_id": arxiv_id.text.strip() if arxiv_id is not None else "",
                "published": published.text.strip()[:10] if published is not None else "",
            }
            papers.append(paper)

        return papers

    def absorb(self):
        """Ejecuta ciclo completo de absorción."""
        todos = []
        for query, categoria in self.QUERIES:
            print(f"[arXiv] Buscando: {categoria}...")
            xml_data = self.search(query)
            if xml_data:
                papers = self.parse_results(xml_data)
                for p in papers:
                    p["categoria_miu"] = categoria
                todos.extend(papers)
                print(f"  → {len(papers)} papers encontrados")

        # Guardar caché
        cache_file = self.cache_dir / f"arxiv_{datetime.now().date()}.json"
        cache_file.write_text(json.dumps(todos, indent=2, ensure_ascii=False))
        print(f"[arXiv] Total absorbido: {len(todos)} papers. Caché: {cache_file}")
        return todos

if __name__ == "__main__":
    fetcher = ArxivFetcher()
    papers = fetcher.absorb()

    # Mostrar resumen
    print(f"
{'='*60}")
    print(f"RESUMEN DE ABSORCIÓN ARXIV — {datetime.now().date()}")
    print(f"{'='*60}")
    for p in papers[:10]:
        print(f"  [{p['categoria_miu']}] {p['title'][:80]}...")
        print(f"       ID: {p['arxiv_id']} | {p['published']}")
