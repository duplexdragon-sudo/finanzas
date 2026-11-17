import json,base64,sys,urllib.request,os
OUT=os.path.dirname(os.path.abspath(__file__))+"/gen/"
S=" Monochrome navy-blue palette (#0C1723 navy-black, #1D3A56 mid blue, #1F4F80 accent), soft studio spotlight, high-end editorial look, sharp focus on subject. No text, no letters, no logos, no watermark."
P={
"a1_statue":("9:16","A classical white-grey marble statue of a bearded seated thinker in a draped toga, chin resting on one hand, typing on a modern silver laptop on his knee, seated on a rectangular stone block, side three-quarter view, full figure visible, isolated on a plain flat pale lavender-white background (#E8E8F4), soft even light, museum photography. No text, no letters, no logos."),
"a2_stage":("1:1","A lone performer in a dark suit seen from behind standing on a stage, arms slightly open, facing a huge dark crowd, a single intense white spotlight beam from above creating haze and glow, cinematic, desaturated cool blue-grey tones. No text, no logos."),
"a3_dancer":("9:16","Full-body photo of a male dancer in a black fedora hat, black jacket, white shirt, black trousers, white socks and black loafers, frozen mid high-kick dance pose, isolated on a plain flat solid pure green background (#00FF00), even studio light, crisp edges, whole body inside frame. Original person, not a celebrity."+S.replace("No text","Background must be flat green. No text")),
"a4_singer":("9:16","Waist-up photo of a male singer with curly dark hair, black blazer over a white graphic t-shirt, singing passionately into a vintage silver microphone held close to his mouth, eyes closed, isolated on a plain flat solid pure green background (#00FF00), even studio light, crisp edges. Original person, not a celebrity. No text, no logos."),
"a5_drummer":("9:16","Full-body photo of a male drummer in a black t-shirt playing a full wooden-finish drum kit with cymbals, sticks raised mid-hit, three-quarter view, entire kit inside frame, isolated on a plain flat solid pure green background (#00FF00), even studio light, crisp edges. Original person, not a celebrity. No text, no logos."),
"a6_leaf":("1:1","A single tropical palm leaf silhouette in solid flat navy blue (#1C2D3E) on a pure white background, flat vector-like, high contrast, top-down, whole leaf inside frame. No text."),
}
model=sys.argv[1]; keys=sys.argv[2:] or list(P)
for k in keys:
  ar,p=P[k]
  body={"contents":[{"parts":[{"text":p}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":ar}}}
  req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",json.dumps(body).encode(),{"Content-Type":"application/json"})
  try: d=json.load(urllib.request.urlopen(req,timeout=240))
  except urllib.error.HTTPError as e: print(k,"HTTP",e.code,e.read()[:200]); continue
  ok=False
  for part in d.get("candidates",[{}])[0].get("content",{}).get("parts",[]):
    if "inlineData" in part:
      open(OUT+k+".png","wb").write(base64.b64decode(part["inlineData"]["data"])); ok=True
  print(k,"OK" if ok else "NOIMG "+str(d)[:200])
