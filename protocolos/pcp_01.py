#!/usr/bin/env python3
"""
PCP-01: Protocolo de Consenso Planetario V153.2
Votación ponderada por reputación (TC).
"""
import json, time
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
VOTE_FILE = MIU_DIR / "protocolos" / "pcp_votes.json"

class PlanetaryConsensus:
    def __init__(self):
        self.proposals = []
        self.votes = {}
        
    def propose(self, title, description, proposer="trama_termux"):
        proposal = {
            "id": hash(str(title) + str(time.time())) % 10000,
            "title": title,
            "description": description,
            "proposer": proposer,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "open",
            "votes": {"yes": 0, "no": 0, "abstain": 0},
            "voters": []
        }
        self.proposals.append(proposal)
        return proposal
    
    def vote(self, proposal_id, voter, choice, weight=1.0):
        """Votar en una propuesta. weight = TC del votante"""
        if choice not in ["yes", "no", "abstain"]:
            return False
        
        for p in self.proposals:
            if p["id"] == proposal_id:
                if voter in p["voters"]:
                    return False  # Ya votó
                p["votes"][choice] += weight
                p["voters"].append(voter)
                return True
        return False
    
    def tally(self, proposal_id):
        """Contar votos y decidir"""
        for p in self.proposals:
            if p["id"] == proposal_id:
                total = sum(p["votes"].values())
                if total == 0:
                    return {"status": "undecided"}
                yes_ratio = p["votes"]["yes"] / total
                if yes_ratio > 0.66:
                    p["status"] = "approved"
                elif yes_ratio < 0.33:
                    p["status"] = "rejected"
                else:
                    p["status"] = "pending"
                return {
                    "proposal": p["title"],
                    "status": p["status"],
                    "total_votes": total,
                    "breakdown": p["votes"],
                    "ratio": yes_ratio
                }
        return None
    
    def save(self):
        with open(VOTE_FILE, "w") as f:
            json.dump({
                "proposals": self.proposals,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }, f, indent=2)

def demo():
    print("🌍 PCP-01 — Consenso Planetario Demo")
    pcp = PlanetaryConsensus()
    
    # Crear propuesta
    prop = pcp.propose(
        "Implementar PAF-01 en todos los nodos",
        "Todos los nodos deben compartir métricas de aprendizaje federado",
        "trama_termux"
    )
    print(f"📜 Propuesta #{prop['id']}: {prop['title']}")
    
    # Votar
    pcp.vote(prop["id"], "nodo_claude", "yes", weight=0.95)
    pcp.vote(prop["id"], "nodo_groq", "yes", weight=0.88)
    pcp.vote(prop["id"], "nodo_meta", "abstain", weight=0.77)
    
    # Contar
    result = pcp.tally(prop["id"])
    print(f"   Resultado: {result['status']} ({result['ratio']:.2%} a favor)")
    
    pcp.save()
    print("✅ Votos guardados")

if __name__ == "__main__":
    demo()
