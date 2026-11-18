import os
HERE=os.path.dirname(os.path.abspath(__file__))
P=lambda *a: os.path.join(HERE,*a)
import json, re, html, base64
d=json.load(open(P('courses.json'),encoding='utf-8'))
LINK=re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
import importlib.util

# reuse url() without rerunning: copy minimal
def url(u):
    if u.startswith('yt:'):
        v=u[3:];t=None
        if '@' in v: v,t=v.split('@')
        return f'https://www.youtube.com/watch?v={v}'+(f'&t={t}' if t else '')
    if u.startswith('ytl:'): return 'https://www.youtube.com/playlist?list='+u[4:]
    if u.startswith('gd:'): return f'https://drive.google.com/file/d/{u[3:]}/view'
    if u.startswith('gf:'): return f'https://docs.google.com/forms/d/e/{u[3:]}/viewform'
    return u
def md(s):
    out='';pos=0
    for m in LINK.finditer(s):
        out+=html.escape(s[pos:m.start()])+f'<a href="{html.escape(url(m.group(2)))}" target="_blank" rel="noopener">{html.escape(m.group(1))}</a>';pos=m.end()
    return out+html.escape(s[pos:])
SRC='https://sites.google.com/view/arilinsmathworld/cursos/'
META={
 'as1':dict(slug='algebra-superior-1',area='alg',ico='ℤ',tag='Álgebra',level='Licenciatura en Matemáticas · Facultad de Ciencias, UNAM',
   by='Arilín Haro y Luis Jorge Sánchez Saldaña',
   intro='Lógica y demostraciones, conjuntos, funciones, inducción, combinatoria y sistemas de ecuaciones. Para más ejemplos y ejercicios se sugiere consultar <em>A Transition to Advanced Mathematics</em> (7.ª ed.) de Douglas Smith, Maurice Eggen y Richard St. Andre.',
   src=SRC+'álgebra-superior-1'),
 'as2':dict(slug='algebra-superior-2',area='alg',ico='ℚ',tag='Álgebra',level='Licenciatura en Matemáticas · Facultad de Ciencias, UNAM',by='',
   intro='La diversión continúa: números enteros, divisibilidad, congruencias, números complejos y polinomios. Cada tema incluye videos, notas y un cuestionario.',
   src=SRC+'álgebra-superior-2'),
 'afc':dict(slug='algebra-fisica',area='alg',ico='ℝ',tag='Álgebra · Física',level='Licenciatura en Física · Facultad de Ciencias, UNAM',by='Arilín Haro',
   intro='Curso de álgebra del programa de la Licenciatura en Física: conjuntos, funciones, matrices y sistemas de ecuaciones, determinantes, números complejos y polinomios.',
   src=SRC+'álgebra-fc'),
 'ga1':dict(slug='geometria-analitica-1',area='geo',ico='△',tag='Geometría',level='Licenciatura · Facultad de Ciencias, UNAM',by='Arilín Haro',
   intro='Material separado en cinco unidades. Para cada tema hay notas, videos y cuestionario, y al final de cada unidad una lista de ejercicios y actividades con GeoGebra y Python. Útil para estudiar o para dar clase 😊.',
   src=SRC+'geometría-analítica-1',
   credits=['Cuestionarios: Sergio Arturo Armendariz Trejo','Listas de ejercicios: Antonio Romero Téllez','Actividades de autoevaluación: Nidia Elizabeth Gómez Ortega','Actividades, preguntas y retos: Sabino Cano']),
 'grupos':dict(slug='teoria-de-grupos',area='alg',ico='G',tag='Álgebra moderna',level='Álgebra Moderna I · En colaboración con el Dr. Luis Jorge Sánchez Saldaña',by='',
   intro='Introducción a la teoría de grupos: permutaciones, grupos, teoremas de isomorfismo, acciones de grupos y teoremas de Sylow. Bibliografía: <em>An Introduction to the Theory of Groups</em>, de Joseph J. Rotman.',
   src='https://sites.google.com/im.unam.mx/luisjorgesanchezsaldana/teaching/teoría-de-grupos',
   credits=['Videos: Luis Jorge Sánchez Saldaña','Notas y videos complementarios: Daniel Guardado Cabral','Cuestionarios: Víctor Eduardo San Martín Macías']),
 'ed1':dict(slug='ecuaciones-diferenciales-1',area='an',ico='∂',tag='Análisis',level='Licenciatura · Facultad de Ciencias, UNAM',by='',
   intro='Material de clase de Ecuaciones Diferenciales I, hecho en tiempo real: notas de clase y ejercicios.',
   src=SRC+'ecuaciones-diferenciales-1',credits=['Material realizado por Alejandro Legaspe']),
 'latex':dict(slug='latex-en-overleaf',area='tool',ico='TeX',tag='Herramientas',level='Para quien empieza a escribir matemáticas',by='Arilín Haro, Luis Jorge Sánchez Saldaña y Leonardo (Nekomath)',
   intro='Más que un curso completo, una ayuda para quienes están aprendiendo a escribir en LaTeX. Los dos primeros videos son un minicurso con lo básico para escribir una tarea bonita; los demás explican cada tema con más detalle.',
   src=SRC+'latex-en-overleaf'),
}
TITLES={'afc':'Álgebra para Física'}
EN={
 'as1':dict(title='Higher Algebra I',tag='Algebra',level="Bachelor's in Mathematics · Faculty of Sciences, UNAM",by='Arilín Haro and Luis Jorge Sánchez Saldaña',
   intro='Logic and proofs, sets, functions, induction, combinatorics and systems of equations. For more examples and exercises, see <em>A Transition to Advanced Mathematics</em> (7th ed.) by Douglas Smith, Maurice Eggen and Richard St. Andre.',
   credits=['Videos and notes by Arilín Haro and Luis Jorge Sánchez Saldaña.','Quizzes by Samuel Restoy Berganza and Arilín Haro.','Practice exercise sheets written by Brenda Navarro Flores.','Worked examples written by Arilín Haro, Luis Jorge Sánchez Saldaña, Brenda Navarro Flores, Luis Fernando García Mora, Antonio Romero Téllez, Porfirio León Álvarez and Samuel Restoy Berganza.']),
 'as2':dict(title='Higher Algebra II',tag='Algebra',level="Bachelor's in Mathematics · Faculty of Sciences, UNAM",
   intro='The fun continues: integers, divisibility, congruences, complex numbers and polynomials. Each topic includes videos, notes and a quiz.',credits=['Quizzes: José Antonio Quiroz']),
 'afc':dict(title='Algebra for Physics',tag='Algebra · Physics',level="Bachelor's in Physics · Faculty of Sciences, UNAM",by='Arilín Haro',
   intro='Algebra course for the Bachelor of Physics program: sets, functions, matrices and systems of equations, determinants, complex numbers and polynomials.',
   credits=['Videos and notes by Arilín Haro and Luis Jorge Sánchez Saldaña.','Quizzes by Samuel Restoy Berganza, Pablo Adrian Hernandez Munguia and Arilín Haro.','Practice exercise sheets written by Antonio Romero Tellez, Brenda Navarro Flores and Arilín Haro.','Worked examples written by Arilín Haro, Luis Jorge Sánchez Saldaña, Brenda Navarro Flores, Luis Fernando García Mora, Antonio Romero Téllez, Porfirio León Álvarez and Samuel Restoy Berganza.']),
 'ga1':dict(title='Analytic Geometry I',tag='Geometry',level='Undergraduate · Faculty of Sciences, UNAM',by='Arilín Haro',
   intro='Materials organized into five units. Each topic has notes, videos and a quiz, and each unit ends with an exercise sheet and activities in GeoGebra and Python. Useful for studying or for teaching 😊.',
   credits=['Quizzes: Sergio Arturo Armendariz Trejo','Exercise sheets: Antonio Romero Téllez','Self-assessment activities: Nidia Elizabeth Gómez Ortega','Activities, questions and challenges: Sabino Cano']),
 'grupos':dict(title='Group Theory',tag='Modern algebra',level='Modern Algebra I · In collaboration with Dr. Luis Jorge Sánchez Saldaña',by='',
   intro='Introduction to group theory: permutations, groups, isomorphism theorems, group actions and the Sylow theorems. Bibliography: <em>An Introduction to the Theory of Groups</em> by Joseph J. Rotman.',
   credits=['Videos: Luis Jorge Sánchez Saldaña','Notes and supplementary videos: Daniel Guardado Cabral','Quizzes: Víctor Eduardo San Martín Macías']),
 'latex':dict(title='LaTeX in Overleaf',tag='Tools',level='For anyone starting to write mathematics',by='Arilín Haro, Luis Jorge Sánchez Saldaña and Leonardo (Nekomath)',
   intro='More than a full course, this is a helping hand for anyone learning to write in LaTeX. The first two videos are a mini course with the basics for writing a nice-looking homework assignment; the rest explain each topic in more detail.',credits=[]),
}
d=[c for c in d if c['id']!='ed1']
# Enlaces de Drive que ya no existen o no son públicos (revisados con el conector de Google Drive).
# Se eliminan de los cursos; ver enlaces_rotos.txt
BROKEN=set(l.strip() for l in open(P('enlaces_rotos.txt'),encoding='utf-8') if l.strip() and not l.startswith('#'))
def _ok(r):
    m=re.search(r'drive\.google\.com/file/d/([\w-]+)',r['u'])
    return not (m and m.group(1) in BROKEN)
def _renum(lst):
    cnt={}
    for r in lst:
        m=re.fullmatch(r'(.*\D) (\d+)',r['t'])
        if m:
            cnt[m.group(1)]=cnt.get(m.group(1),0)+1
            r['t']=f"{m.group(1)} {cnt[m.group(1)]}"
    return lst
REMOVED=0
for c in d:
    for u in c['units']:
        for t in u['topics']:
            n=len(t['res']); t['res']=_renum([r for r in t['res'] if _ok(r)]); REMOVED+=n-len(t['res'])
        for k in ('material','activities'):
            n=len(u[k]); u[k]=_renum([r for r in u[k] if _ok(r)]); REMOVED+=n-len(u[k])
print('enlaces eliminados:',REMOVED)
FIX={'Triángulo de Pasca':'Triángulo de Pascal','EJERCICIOS DE PRÁCTICA':'Ejercicios de práctica','Cuest1':'Cuestionario 1','Cuest2':'Cuestionario 2','notas':'Más notas','ejercicios':'Más ejercicios','Acvt. Geogebra':'GeoGebra','+Ejercicios':'Más ejercicios'}
for c in d:
    for u in c['units']:
        for r in [r for t in u['topics'] for r in t['res']]+u['material']+u['activities']:
            r['t']=FIX.get(r['t'],r['t'])
# Notas de los videos (../notas/notas.json, ver ../notas/CONVENCIONES.md): se agregan como t['nb'] al tema
NB=json.load(open(P('../notas/notas.json'),encoding='utf-8')) if os.path.exists(P('../notas/notas.json')) else []
NB_USADAS=0
out=[]
for c in d:
    m=META[c['id']]
    for e in NB:
        if e['curso']!=m['slug'] or c['id'] in ('ed1',):continue
        us=c['units']
        ts=[t for t in us[e['unidad']-1]['topics'] if t['title']==e['tema']] if e['unidad']<=len(us) else []
        if len(ts)!=1:raise SystemExit('notas.json: no encuentro el tema %r en %s unidad %d'%(e['tema'],e['curso'],e['unidad']))
        ruta='notas/%s/%s'%(e['curso'],e['slug'])
        for ext in ('html','pdf'):
            if not os.path.exists(P('../'+ruta+'.'+ext)):raise SystemExit('Falta '+ruta+'.'+ext)
        ts[0].setdefault('nb',[]).append({'video':e['video'],'src':ruta+'.html','pdf':ruta+'.pdf'})
        ts[0]['nb'].sort(key=lambda x:x['video']);NB_USADAS+=1
    units=[]
    for u in c['units']:
        notes=[md(n) for n in u['notes'] if not (c['id']=='ed1')]
        units.append({'title':re.sub(r'^Unidad \d+\.\s*','',u['title']),'topics':u['topics'],'mat':u['material'],'act':u['activities'],'notes':notes})
    out.append({'id':m['slug'],'title':TITLES.get(c['id'],c['title']),'area':m['area'],'ico':m['ico'],'tag':m['tag'],'level':m['level'],'by':m['by'],
      'intro':m['intro'],'video':c['video'],'src':m['src'],'credits':m.get('credits') or [md(x) for x in c['credits']],'units':units,'en':EN[c['id']]})
js=json.dumps(out,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
img='data:image/webp;base64,'+base64.b64encode(open(P('retrato.webp'),'rb').read()).decode()
t=open(P('template.html'),encoding='utf-8').read()
t=t.replace('__DATA__',js).replace('__RETRATO__',img)
import sys; sys.path.insert(0,HERE)
from tr_en import TR
a=t.index('<main data-lang="es" lang="es">');b=t.index('</main>',a)+7
es=t[a:b]
en=es.replace('<main data-lang="es" lang="es">','<main data-lang="en" lang="en" hidden>')
en=re.sub(r'\bid="([^"]+)"',lambda m:f'id="{m.group(1)}-en"',en)
def sub_text(m):
    pre,txt,post=m.group(1),m.group(2),m.group(3)
    k=txt.strip()
    if k in TR: return pre+txt.replace(k,TR[k])+post
    return m.group(0)
en=re.sub(r'(>)([^<>]+)(<)',sub_text,en)
def sub_attr(m):
    v=m.group(2); return m.group(1)+'="'+TR.get(v,v)+'"'
en=re.sub(r'\b(alt|aria-label|placeholder)="([^"]*)"',sub_attr,en)
en=en.replace('Materials to <em>teaching</em>','Materials to <em>teach</em>').replace('href="https://museoarilinsmath.com/prensa"','href="https://museoarilinsmath.com/en/prensa"')
for x,y in [('Clases de GeoGebra','GeoGebra lessons'),('Actividades de Geometría Analítica','Analytic Geometry activities'),('Matemáticas con Python','Mathematics with Python'),('Finanzas con propósito','Finance with Purpose')]:
    en=en.replace('&nbsp;/&nbsp; '+x,'&nbsp;/&nbsp; '+y)
t=t[:b]+'\n'+en+t[b:]
open(P('..','index.html'),'w',encoding='utf-8').write(t)
tot=lambda k:sum(1 for c in out for u in c['units'] for tp in u['topics'] for r in tp['res'] if r['k']==k)
print(len(t), 'videos',tot('v'),'notas',tot('n'),'cuest',tot('q'))
