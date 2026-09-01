import json, math, time
class LODC20Predictor:
    def __init__(self, mean_c20=-4.841695804933607e-04, Ktau=34.0332, r_lod=-0.868):
        self.mean_c20=mean_c20; self.Ktau=Ktau; self.r_lod=r_lod
    def predict(self, c20):
        dc=c20-self.mean_c20
        return self.r_lod*dc*1e9*(self.Ktau/100)
    def run(self, c20_test=-4.841694e-04):
        p=self.predict(c20_test)
        return {"c20_input":c20_test,"delta_c20":c20_test-self.mean_c20,
                "lod_prediction_ms":p,"phi_clima":abs(p)*self.Ktau/100,
                "timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ"),"version":"V153"}
if __name__=="__main__":
    print(json.dumps(LODC20Predictor().run(), indent=2))
