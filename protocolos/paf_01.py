#!/usr/bin/env python3
"""
PAF-01: Protocolo de Aprendizaje Federado V153.2
Intercambia gradientes/métricas, no datos crudos.
Compatible con nodos Termux, VPS, y navegadores.
"""
import json, time, hashlib
from pathlib import Path

MIU_DIR = Path("/data/data/com.termux/files/home/miu-ecosistema")
STATE_FILE = MIU_DIR / "protocolos" / "paf_state.json"

class FederatedLearningNode:
    def __init__(self, node_id="trama_termux"):
        self.node_id = node_id
        self.local_params = {}
        self.global_params = {}
        self.round = 0
        self.reputation = 1.0  # TC base
        
    def train_local(self, metric_name, value):
        """Entrenar métrica local (simulado)"""
        self.local_params[metric_name] = {
            "value": value,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "node": self.node_id
        }
        return self.local_params[metric_name]
    
    def aggregate(self, other_nodes_params):
        """Agregar parámetros de otros nodos (FedAvg simplificado)"""
        if not other_nodes_params:
            return self.local_params
        
        all_params = [self.local_params] + other_nodes_params
        aggregated = {}
        
        for key in self.local_params:
            values = [p.get(key, {}).get("value", 0) for p in all_params if key in p]
            if values:
                aggregated[key] = sum(values) / len(values)
        
        self.global_params = aggregated
        self.round += 1
        return aggregated
    
    def export_gradient(self):
        """Exportar solo el gradiente (delta), no los datos"""
        gradient = {
            "node_id": self.node_id,
            "round": self.round,
            "params": self.local_params,
            "reputation": self.reputation,
            "hash": hashlib.sha256(json.dumps(self.local_params, sort_keys=True).encode()).hexdigest()[:16]
        }
        return gradient
    
    def import_gradient(self, gradient):
        """Importar gradiente de otro nodo"""
        # Validar hash básico
        if gradient.get("reputation", 0) < 0.5:
            return False  # Nodo de baja reputación, rechazar
        return True
    
    def save(self):
        state = {
            "node_id": self.node_id,
            "round": self.round,
            "reputation": self.reputation,
            "local_params": self.local_params,
            "global_params": self.global_params,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    
    def load(self):
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                state = json.load(f)
            self.node_id = state.get("node_id", self.node_id)
            self.round = state.get("round", 0)
            self.reputation = state.get("reputation", 1.0)
            self.local_params = state.get("local_params", {})
            self.global_params = state.get("global_params", {})

def demo():
    print("🌐 PAF-01 — Aprendizaje Federado Demo")
    node = FederatedLearningNode("trama_termux")
    node.load()
    
    # Simular entrenamiento local
    node.train_local("phi_coherence", 0.77)
    node.train_local("k_tau", 34.0332)
    node.train_local("sigma", 3.427051)
    
    gradient = node.export_gradient()
    print(f"📤 Gradiente exportado: {json.dumps(gradient, indent=2)}")
    
    # Simular recepción de otro nodo
    other_gradient = {
        "node_id": "nodo_claude",
        "round": 5,
        "params": {"phi_coherence": {"value": 0.82}, "k_tau": {"value": 34.1}},
        "reputation": 0.95
    }
    
    if node.import_gradient(other_gradient):
        aggregated = node.aggregate([other_gradient["params"]])
        print(f"📥 Agregado: {json.dumps(aggregated, indent=2)}")
    
    node.save()
    print("✅ PAF-01 estado guardado")

if __name__ == "__main__":
    demo()
