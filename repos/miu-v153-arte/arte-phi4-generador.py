import json, math, random
class ArtePhi4:
    def __init__(self, N=64, phi=1.618033988749895):
        self.N = N; self.phi = phi
        self.field = [[0.0 for _ in range(N)] for _ in range(N)]
    def seed(self, density=0.15):
        for i in range(self.N):
            for j in range(self.N):
                if random.random()<density: self.field[i][j]=random.uniform(-1,1)
    def evolve(self, steps=20):
        for _ in range(steps):
            nf = [row[:] for row in self.field]
            for i in range(self.N):
                for j in range(self.N):
                    laplace=0
                    for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ni,nj=(i+di)%self.N,(j+dj)%self.N
                        laplace+=self.field[ni][nj]-self.field[i][j]
                    pot=4*self.field[i][j]*(self.field[i][j]**2-1)
                    nf[i][j]+=0.1*(laplace-pot)
            self.field=nf
    def measure(self):
        return sum((self.field[i][j]**2-1)**2 for i in range(self.N) for j in range(self.N))/(self.N**2)
    def to_svg(self, fn="arte_phi4.svg"):
        mv=min(min(r) for r in self.field); Mv=max(max(r) for r in self.field)
        rng=Mv-mv if Mv!=mv else 1; sz=512; c=sz//self.N
        lines=['<svg xmlns="http://www.w3.org/2000/svg" width="'+str(sz)+'" height="'+str(sz)+'" style="background:#0a0a0b">']
        for i in range(self.N):
            for j in range(self.N):
                v=(self.field[i][j]-mv)/rng
                r=int(10+245*v); g=int(50+150*(1-v)); b=int(200+55*v)
                lines.append('<rect x="'+str(j*c)+'" y="'+str(i*c)+'" width="'+str(c)+'" height="'+str(c)+'" fill="rgb('+str(r)+','+str(g)+','+str(b)+')"/>')
        lines.append('</svg>')
        with open(fn,'w') as f: f.write('\n'.join(lines))
        return fn
    def run(self):
        self.seed(); self.evolve()
        pr=self.measure()
        return {"N":self.N,"phi":self.phi,"phi_rem":pr,"phi_est":pr*self.phi,
                "onda_auto":1.0/(1+pr),"timestamp":__import__('time').strftime("%Y-%m-%dT%H:%M:%SZ"),"version":"V153"}
if __name__=="__main__":
    a=ArtePhi4(); r=a.run(); a.to_svg(); r["svg_generated"]="arte_phi4.svg"
    print(json.dumps(r, indent=2))
