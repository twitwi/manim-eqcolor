
from manim import *

TEX_TEMPLATE = r'''\usepackage{xcolor}'''

def eq(content, **kw_args):
    if 'tex_template' not in kw_args:
        kw_args['tex_template'] = TexTemplate()
    if type(kw_args['tex_template']) == str:
        ttpl = TexTemplate()
        ttpl.add_to_preamble(kw_args['tex_template'])
        kw_args['tex_template'] = ttpl
    kw_args['tex_template'].add_to_preamble(TEX_TEMPLATE)
        
    lines = [l for l in content.split('\n') if len(l.strip()) > 0]
    il = 0
    chunks = []
    gpre = []
    gpost = []
    glines = []
    gmore = []
    while il < len(lines):
        l = lines[il]
        if l.startswith('%%'): # magic command
            command = l[2:]
            il+=1
            c, p = command.split(':', 1)
            p = p.strip()
            if c == 'cause':
                #&\\phantom{"+"".join(stack)+"}\\;{\\color{lightgray}\\downarrow{}\\;{\\small \\text{", REST, "}}} \\nonumber\\\\
                gmore[-1].append(['cause', len(chunks)])
                chunks.append(r'&\; \downarrow{}\;{\tiny \text{' + p + r'}} \nonumber \\')
            if c == 'up':
                gmore[-1].append(['up', int(p)])
            # TODO maybe add stack stuff... but not sure as the latex rendering and the metalatex rendering will be different (in addition to causes)
        else: # 2-3 lines
            if il==0:
                pre = ''
                eq, post = lines[il:il+2]
                il+=2
            elif il==len(lines)-2:
                pre, eq = lines[il:il+2]
                post = ''
                il+=2
            else:
                pre, eq, post = lines[il:il+3]
                il+=3
            mlen = max(len(pre), len(post))
            pre += ' ' * (mlen - len(pre))
            post += ' ' * (mlen - len(post))
            pre = pre.replace('%', ' ')
            post = post.replace('%', ' ')

            splitlocs = set()
            for sep in '() [] <> {}'.split():
                op,cl = sep
                for i in range(len(post)):
                    if pre[i] == op or post[i] == op:
                        splitlocs.add(i)
                    if pre[i] == cl or post[i] == cl:
                        splitlocs.add(i+1)
            splitlocs = [*sorted(list(splitlocs)), len(eq)]
            base_chunk = len(chunks)
            for iloc in range(len(splitlocs)):
                start = 0 if iloc == 0 else splitlocs[iloc-1]
                end = splitlocs[iloc]
                chunks.append(eq[start:end])

            gpre.append([])
            gpost.append([])
            gmore.append([])
            for sep in '() [] <> {}'.split():
                op,cl = sep
                gpre[-1].append([])
                inside = False
                for ichunk, i in enumerate(splitlocs):
                    if i>=len(pre): break
                    if pre[i-1] == cl: inside = False
                    if pre[i] == op: inside = True
                    if inside: gpre[-1][-1].append(base_chunk+ichunk+1)
                gpost[-1].append([])
                inside = False
                for ichunk, i in enumerate(splitlocs):
                    if i>=len(post): break
                    if post[i-1] == cl: inside = False
                    if post[i] == op: inside = True
                    if inside: gpost[-1][-1].append(base_chunk+ichunk+1)
            
            glines.append(list(range(base_chunk, len(chunks))))

    return MathTex(*chunks, **kw_args), gpre, gpost, glines, gmore


def eqanimate(scene, tex, gpre, gpost, glines, gmore, COLORS=[BLUE, RED, GREEN, YELLOW], WHITE=WHITE, rt=1, trim=None):
    if trim is not None:
        if type(trim) == int: trim = [trim]
        if len(trim) == 1: trim.append(0)
        N = len(gpre)
        if trim[1] == 0: trim[1] = N
        gpre = gpre[trim[0] : trim[1]]
        gpost = gpost[trim[0] : trim[1]]
        glines = glines[trim[0] : trim[1]]
        gmore = gmore[trim[0] : trim[1]]
    gpre = gpre[1:]
    for i,_ in enumerate(gpre):
        enter1 = []
        enter2 = []
        leave = []
        for j,group in enumerate(gpost[i]):
            if len(group) > 0:
                for ind in group:
                    enter1.append(ApplyMethod(tex.submobjects[ind].set_fill, COLORS[j]))
                    leave.append(ApplyMethod(tex.submobjects[ind].set_fill, WHITE))
        for j,group in enumerate(gpre[i]):
            if len(group) > 0:
                e2 = []
                for ind in group:
                    tex.submobjects[ind].set_fill(COLORS[j]) # set the color before fading in
                    e2.append(GrowFromCenter(tex.submobjects[ind]))
                    leave.append(ApplyMethod(tex.submobjects[ind].set_fill, WHITE))
                enter2.append(AnimationGroup(*e2))
        # show the first line
        if i == 0: scene.play(FadeIn(*[tex.submobjects[ind] for ind in glines[i]], run_time=rt))
        # highlight current line
        if len(enter1)>0: scene.play(AnimationGroup(*enter1), run_time=rt)
        for c,rest in gmore[i]:
            if c == 'cause':
                tex.submobjects[rest].set_fill(GREY)
                scene.play(FadeIn(tex.submobjects[rest]), run_time=rt)
            elif c == 'up':
                scene.play(scene.camera.frame.animate.shift(rest*DOWN))
        # show non-highlight of next line
        toshow = [tex.submobjects[ind] for ind in glines[i+1] if ind not in sum(gpre[i], [])]
        if len(toshow)>0: scene.play(FadeIn(*toshow, run_time=rt))
        # show highlight of next line
        #if len(enter2)>0: scene.play(AnimationGroup(*enter2, run_time=rt))
        for e in enter2: scene.play(e, run_time=rt)
        #self.wait(1)
        # unhighlight
        if len(leave)>0: scene.play(AnimationGroup(*leave), run_time=rt)
