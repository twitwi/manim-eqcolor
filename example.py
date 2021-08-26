from manim import *
from manim_eqcolor import *

class Example(MovingCameraScene): # need MovingCameraScene for shifting the equations up
    def construct(self):
        info = eq(r'''
A &= 1 + 2 + 3 + 4 + \cdots \\
%    (   )
%%cause: we define matching groups
%  ()
&= 3 + 3 + 4 + \cdots \\
%  (       )   [    ]
%%cause: we can have several groups
%  ()   [                             ]
&= 10 + 5 + 6 + 7 + 8 + 9 + 10 + \cdots \\
%  ()   [   ]           []  ()
%%cause: a group can be split
%  ()   []
&= 20 + 20 + 7 + 8 + \cdots \\
%  ()   []   <>  {}
%%cause: there are 4 colors (let's make some pace first)
%%up: 4
%  {}  <>  []   ()
&= 8 + 7 + 20 + 20 + \cdots \\
%  []  <>  (     ) {      }
%%cause: the colors appear always in the same order
%%cause: and there is no contraint to have the same color in the two lines
%  ()   <>  []
&= 40 + 7 + 8 + \cdots \\
%
%%cause: using some custom commands
%
&= \yeah
''', tex_template=r'''
\newcommand{\yeah}{\textbf{The End}}
''')
        # it is big so let's shift it
        info[0].align_on_border(UP)
        # let's animate it!
        eqanimate(self, *info)
