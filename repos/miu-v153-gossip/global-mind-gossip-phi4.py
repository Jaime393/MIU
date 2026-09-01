import json, math, random, time
class GossipPhi4:
    def __init__(self, N=140, sigma=3.427051):
        self.N = N; self.sigma = sigma; self.phi = (1+math.sqrt(5))/2; self.nodes = []
    def spin(self):
        if not self.nodes:
            self.nodes = [{"id":i,"state":random.random(),"energy":0} for i in range(self.N)]
        for node in self.nodes:
            neighbors = [self.nodes[(node["id"]+d)%self.N] for d in (-1,1)]
            coupling = sum(n["state"]-node["state"] for n in neighbors)
            node["energy"] = (node["state"]**2-1)**2 + self.sigma*coupling
            node["state"] += 0.01*(-4*node["state"]*(node["state"]**2-1)+self.sigma*coupling)
            node["state"] = max(-2.0, min(2.0, node["state"]))
        states = [n["state"] for n in self.nodes]
        mean_s = sum(states)/len(states)
        var = sum((s-mean_s)**2 for s in states)/len(states)
        return self.N*math.log(self.N+1)*(1-math.exp(-var/self.sigma))
    def run(self, cycles=100):
        phis = [self.spin() for _ in range(cycles)]
        return {"N":self.N,"sigma":self.sigma,"phi":self.phi,
                "phi_global_mean":sum(phis)/len(phis),"phi_global_last":phis[-1],
                "O_log_N":math.log(self.N),"cycles":cycles,
                "timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ"),"version":"V153"}
if __name__=="__main__":
    print(json.dumps(GossipPhi4().run(), indent=2))
