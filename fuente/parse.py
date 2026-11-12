import os
HERE=os.path.dirname(os.path.abspath(__file__))
import re, json, sys
R=os.path.join(HERE,'raw')+'/'
LINK=re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
RK={'0B42ihcbfBy7cRmJRVFUyU1hGUDBlOVQ5VUEtVlhuZlo4bF9B':'0-LjT_KkFUtOLuApnt-_tbbg',
    '0B42ihcbfBy7cdnc3UnZBVUNjQ1lMYnFVRXdPWUIxMFBqUmFN':'0-U-T2wQHlPpgLd8AQ0ujDzQ',
    '0B42ihcbfBy7cRHFhSkJqRlJfd3JfVGZWRGt1R1ctTjBYbWNz':'0-AAE2eazk67U7K3qkgWY7BA'}
def url(u):
    if u.startswith('yt:'):
        v=u[3:]; t=None
        if '@' in v: v,t=v.split('@')
        return f'https://www.youtube.com/watch?v={v}'+(f'&t={t}' if t else '')
    if u.startswith('ytl:'): return 'https://www.youtube.com/playlist?list='+u[4:]
    if u.startswith('gd:'):
        i=u[3:]; return f'https://drive.google.com/file/d/{i}/view'+(f'?resourcekey={RK[i]}' if i in RK else '')
    if u.startswith('gf:'): return f'https://docs.google.com/forms/d/e/{u[3:]}/viewform'
    return u
def kind(u,label):
    l=label.lower()
    if u.startswith(('yt:','ytl:')) or 'video' in l: return 'v'
    if u.startswith('gf:') or 'forms' in u or 'cuest' in l: return 'q'
    if 'geogebra' in u or 'colab' in u or 'desmos' in u: return 'a'
    if 'ejercicio' in l or 'overleaf' in u: return 'e'
    return 'n'
SING={'videos':'Video','video':'Video','notas':'Notas','notas de clase':'Notas','cuestionario':'Cuestionario','ejercicios':'Ejercicios','video complementario':'Video complementario','videos alternativos':'Video alternativo','videos de arilín':'Video de Arilín','v.a':'Notas (versión alternativa)','más ejemplos':'Más ejemplos','cuestionario de la unidad':'Cuestionario de la unidad','actv. geogebra':'GeoGebra','actidades en geogebra':'GeoGebra','ejercicios de repaso':'Ejercicios de repaso'}
def res(line):
    """parse a line into list of {t,u,k}"""
    out=[];pos=0;label=''
    for m in LINK.finditer(line):
        txt=line[pos:m.start()]
        seg=re.sub(r'^[\s,\-:+.]+|[\s,\-:+.]+$','',txt).strip()
        if seg:
            mm=re.search(r'(Videos de Arilín|Videos alternativos|Video complementario|Notas de Clase|Más ejemplos|Actv\. Geogebra|Actidades en Geogebra|Videos?|Notas|Cuestionario|Ejercicios|v\.a)\s*$',seg,re.I)
            if mm: label=mm.group(1)
            else:
                parts=[p.strip() for p in seg.split(':') if p.strip()]
                label=parts[-1] if parts else seg
        t,u=m.group(1).strip(),m.group(2)
        lab=SING.get(label.lower().rstrip(':').strip(), label)
        if re.fullmatch(r'\d+( y \d+)?',t): name=f'{lab} {t}'.strip()
        else: name=t.rstrip(',')
        out.append({'t':name,'u':url(u),'k':kind(u,name)})
        pos=m.end()
    return out
def lead(line):
    m=LINK.search(line); return (line[:m.start()] if m else line)
def nolinks(line): return LINK.sub(lambda m:m.group(1),line)

RESLAB=re.compile(r'^(Videos?|Notas( de Clase)?|Cuestionario|Video complementario)\b',re.I)
def new_unit(C,title): C['units'].append({'title':title.strip().rstrip('.'),'topics':[],'material':[],'activities':[],'notes':[]})

def generic(key, title, start, credits_marker):
    lines=open(R+key+'.txt',encoding='utf-8').read().split('\n')
    C={'id':key,'title':title,'intro':[],'video':None,'units':[],'credits':[]}
    mode='intro';pend=[];cur=None
    def topic(t):
        nonlocal cur
        if not C['units']: new_unit(C,'Temas')
        cur={'title':re.sub(r'(\s*(Notas|Videos?|:))+\s*$','',t.strip()).strip(),'res':[]};C['units'][-1]['topics'].append(cur)
    def flush_as_units():
        nonlocal pend
        for p in pend: new_unit(C,p)
        pend=[]
    for raw in lines:
        L=raw.strip()
        if not L: continue
        if mode=='intro':
            if L.startswith(start): mode='body'
            else:
                if L.startswith('VIDEO '): C['video']=url(L[6:])
                elif not L.startswith('#1 '+title.split()[0]) and not re.match(r'#1 ',L): C['intro'].append(L)
                continue
        if credits_marker and L.startswith(credits_marker): mode='credits'; continue
        if mode=='credits': C['credits'].append(L.lstrip('- ')); continue
        hm=re.match(r'#(\d) (.*)',L)
        body=L[2:] if L.startswith('- ') else (hm.group(2) if hm else L)
        has=bool(LINK.search(body))
        # explicit units
        if hm and hm.group(1) in '12' and not has:
            pend=[];new_unit(C,body);cur=None;continue
        if re.match(r'^\d+\.\S',body) and not has:  # "1.Introducción"
            pend=[];new_unit(C,re.sub(r'^\d+\.','',body));cur=None;continue
        if re.match(r'(?i)no hay videos',body): continue
        if re.match(r'(?i)(actividades, preguntas y retos)',body):
            mode_act=True; C['units'][-1]['_act']=True; continue
        isres=bool(RESLAB.match(body))
        ismat=bool(re.match(r'(?i)^(\[?ejercicios|\[actividad de autoevaluaci|cuestionario de la unidad|\[?EJERCICIOS)',body)) or (hm and hm.group(1)=='3' and has)
        if ismat:
            if pend:
                for p in pend: topic(p)
                pend=[]
            r=res(body)
            if 'CUESTIONARIO DE LA UNIDAD' in body: 
                for x in r: x['t']=x['t'].replace('Cuestionario de la unidad','Cuestionario de la unidad'); x['k']='q'
            C['units'][-1]['material']+=r
            if not r and body.strip():
                pass
            continue
        if not has and not isres and len(body)>100:
            if pend: flush_as_units()
            (C['units'][-1]['notes'] if C['units'] else C['intro']).append(body); continue
        if not has and not isres:
            if C['units'] and C['units'][-1].get('_act') and False: pass
            pend.append(re.sub(r'^\d+\.\s*','',body)); continue
        if C['units'] and C['units'][-1].get('_act') and not L.startswith('- ') and not isres:
            C['units'][-1]['activities']+=res(body); continue
        if isres:
            if pend:
                if len(pend)>=2:
                    for p in pend[:-1]: new_unit(C,p)
                topic(pend[-1]); pend=[]
            if cur is None: topic('Material')
            cur['res']+=res(body); continue
        # line with links, not a resource label
        ld=re.sub(r'(Notas)?\s*$','',lead(body)).strip()
        if L.startswith('- ') and ld and len(ld)<110 and not ld.lower().startswith('para profundizar') and not ld.lower().startswith('videos y notas'):
            if pend: flush_as_units()
            topic(ld); cur['res']+=res(body); continue
        # note
        if pend: flush_as_units()
        if not C['units']: C['intro'].append(L)
        else: C['units'][-1]['notes'].append(body)
    for p in pend: (C['units'][-1]['notes'] if C['units'] else C['intro']).append(p)
    for u in C['units']: u.pop('_act',None)
    return C

def latex():
    C={'id':'latex','title':'LaTeX en Overleaf','intro':[],'video':None,'units':[],'credits':[]}
    lines=open(R+'latex.txt',encoding='utf-8').read().split('\n')
    C['intro'].append(lines[1])
    new_unit(C,'Minicurso de iniciación en LaTeX y Overleaf')
    C['units'][-1]['topics'].append({'title':'Minicurso (2 partes)','res':res(lines[2])})
    new_unit(C,'Por temas')
    for L in lines[4:]:
        r=res(L[2:]); C['units'][-1]['topics'].append({'title':r[0]['t'],'res':[{'t':'Ver video','u':r[0]['u'],'k':'v'}]})
    return C

out=[]
out.append(generic('as1','Álgebra Superior I','- Lógica','#3 Agradecimientos'))
out.append(generic('as2','Álgebra Superior II','- Números Enteros','Agracedimientos'))
out.append(generic('afc','Álgebra (Física)','- Conjuntos y Relaciones','#3 Agradecimientos'))
out.append(generic('ga1','Geometría Analítica I','#2 Unidad 1','Agradecimientos'))
out.append(generic('ed1','Ecuaciones Diferenciales I','1.Introducción',None))
out.append(generic('grupos','Teoría de grupos','#1 Permutaciones',None))
out.append(latex())
json.dump(out,open(os.path.join(HERE,'courses.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
for c in out:
    print('==',c['title'],'| video:',bool(c['video']),'| intro',len(c['intro']),'| credits',len(c['credits']))
    for u in c['units']:
        print('  U:',u['title'][:60],'| topics',len(u['topics']),'mat',len(u['material']),'act',len(u['activities']),'notes',len(u['notes']))
        for t in u['topics']: print('     -',t['title'][:60],'·',len(t['res']), ','.join(sorted(set(r['k'] for r in t['res']))))
