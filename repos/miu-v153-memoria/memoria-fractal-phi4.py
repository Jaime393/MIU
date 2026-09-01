import json, math, random, time
class MemoriaFractal:
    def __init__(self, phi_prev=187.04, decay=0.95):
        self.phi = phi_prev; self.decay = decay; self.memories = []; self.hub = None
    def record(self, stimulus):
        m = {"id":len(self.memories),"stimulus":stimulus,
             "weight":math.log(1+abs(stimulus))*self.phi/100,"access_count":1,"born":time.time()}
        self.memories.append(m); self._rebalance(); return m
    def forget(self, threshold=0.05):
        deleted = [m for m in self.memories if m["weight"]<threshold]
        self.memories = [m for m in self.memories if m["weight"]>=threshold]
        return deleted
    def _rebalance(self):
        if not self.memories: return
        self.memories.sort(key=lambda m:m["access_count"]*m["weight"], reverse=True)
        self.hub = self.memories[0]["id"] if self.memories else None
        for m in self.memories[:len(self.memories)//3]: m["access_count"] += 1
    def phi_net(self):
        if not self.memories: return 0.0
        tw = sum(m["weight"]*m["access_count"] for m in self.memories)
        probs = [m["weight"]/tw for m in self.memories if tw>0]
        entropy = -sum(p*math.log(p) for p in probs if p>0)
        return entropy*math.log(len(self.memories)+1)*self.phi/100
    def run(self, n_stimuli=50):
        for i in range(n_stimuli): self.record(random.gauss(0,1))
        deleted = self.forget(0.05)
        return {"phi_prev":self.phi,"memories_alive":len(self.memories),
                "memories_deleted":len(deleted),"hub":self.hub,
                "phi_net":self.phi_net(),"phi_new":self.phi_net()+self.phi,
                "neto":self.phi_net(),"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ"),"version":"V153"}
if __name__=="__main__":
    print(json.dumps(MemoriaFractal().run(), indent=2))
