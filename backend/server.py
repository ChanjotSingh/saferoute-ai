import json,math,mimetypes,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
R=Path(__file__).resolve().parent.parent
A=json.loads((R/'model/us_accidents_model.json').read_text())
W=A['weather_groups']; B=A['boolean_features']
def n(v,d,l,h):
 try:return max(l,min(h,float(v)))
 except (TypeError,ValueError):return d
def wg(v):
 s=str(v or '').lower()
 if any(x in s for x in ('rain','drizzle','thunder')):return 'rain'
 if any(x in s for x in ('snow','sleet','hail')):return 'snow'
 if any(x in s for x in ('fog','mist','haze','smoke')):return 'fog'
 if 'clear' in s or 'fair' in s:return 'clear'
 if 'cloud' in s or 'overcast' in s:return 'cloud'
 return 'other'
def predict(r):
 h=int(n(r.get('hour'),12,0,23)); w=wg(r.get('weather')); road=str(r.get('road','arterial')).lower(); f={k:False for k in B};f['Junction']=road=='junction';f['Traffic_Signal']=road=='arterial';f['Stop']=road=='local'
 x=[1,math.sin(2*math.pi*h/24),math.cos(2*math.pi*h/24),math.sin(4*math.pi/7),math.cos(4*math.pi/7),n(r.get('temperature'),60,-30,130)/130,n(r.get('humidity'),60,0,100)/100,n(r.get('pressure'),29.8,25,33)/33,n(r.get('visibility'),10,0,30)/30,n(r.get('wind_speed'),5,0,100)/100,n(r.get('precipitation'),0,0,10)/10,n(r.get('distance'),0,0,100)/100]+[float(f[k]) for k in B]+[float(w==k) for k in W]
 z=[sum(v*q[j] for v,q in zip(x,A['weights'])) for j in range(3)];m=max(z);e=[math.exp(v-m) for v in z];p=[v/sum(e) for v in e];labs=['Low','Moderate','High'];fac=[]
 if h in (7,8,9,17,18,19):fac+=['Peak commute']
 if w in ('rain','snow','fog'):fac+=['Reduced weather visibility']
 if road=='junction':fac+=['Junction context']
 return {'risk_score':round(p[1]*50+p[2]*100),'risk_level':labs[p.index(max(p))],'probabilities':dict(zip(labs,[round(v,4) for v in p])),'factors':fac or ['Current scenario inputs'],'model':'US Accidents March 2023 multinomial logistic regression','validation':A['metrics'],'note':'Academic decision-support model; not for operational road-safety decisions.'}
class H(BaseHTTPRequestHandler):
 def out(self,c,x):
  d=json.dumps(x).encode();self.send_response(c);self.send_header('Content-Type','application/json');self.send_header('Access-Control-Allow-Origin','*');self.send_header('Content-Length',str(len(d)));self.end_headers();self.wfile.write(d)
 def do_OPTIONS(self):self.send_response(204);self.send_header('Access-Control-Allow-Origin','*');self.send_header('Access-Control-Allow-Headers','Content-Type');self.end_headers()
 def do_POST(self):
  if self.path!='/predict':return self.out(404,{'error':'Not found'})
  try:self.out(200,predict(json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))))
  except (ValueError,json.JSONDecodeError) as e:self.out(400,{'error':str(e)})
 def do_GET(self):
  if self.path=='/health':return self.out(200,{'status':'ok','model':A['model'],'dataset':A['dataset'],'validation':A['metrics']})
  if self.path=='/hotspots':return self.out(200,{'hotspots':A['hotspots'],'dataset':A['dataset']})
  p=(R/(self.path.split('?',1)[0].lstrip('/') or 'index.html')).resolve()
  if R not in p.parents or not p.is_file():return self.out(404,{'error':'Not found'})
  d=p.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(str(p))[0] or 'application/octet-stream');self.send_header('Content-Length',str(len(d)));self.end_headers();self.wfile.write(d)
 def log_message(self,*a):pass
ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8001'))),H).serve_forever()
