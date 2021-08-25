

## Example (non-minimal)

In a file (e.g., `test-eqcolor.py`), we put

~~~python3
from manim import *
from manim_eqcolor import *

class Example(Scene):
    def construct(self):
        info = eq(r'''
&=\innprod{\Cm}{T^\epsilon} - \innprod{\Cm}{T^0} + \epsilon \entropy{T^\epsilon} - \epsilon \entropy{T^\epsilon} \\
% (                       )                      (                             )
%%cause: by definition of $T^\epsilon$ that minimizes $\innprod{\Cm}{T} + \epsilon \entropy{T}$
%     (                 )                         (                    )
&\leq \innprod{\Cm }{T^0} - \innprod{\Cm }{T^0} + \epsilon \entropy{T^0} - \epsilon \entropy{T^\epsilon} \label{eq_lemma:2a} \\
%     [                 ]                         {                    }
%%cause: shuffling just for the demo/test
%     {                    }                         [                 ]
&\leq \epsilon \entropy{T^0} - \innprod{\Cm }{T^0} + \innprod{\Cm }{T^0} - \epsilon \entropy{T^\epsilon} \\
%     (      ) <           > [                                         ] <>(      ) <                  >
%%cause: simplifying and factorizing
%     (      ) <                                                 >
&\leq \epsilon \left( \entropy{T^0} - \entropy{T^\epsilon} \right) 
''', tex_template=r'''
\newcommand{\Cm}{\textbf{C}}
\newcommand{\entropy}[1]{\mathcal{H}(#1)}
\newcommand{\innprod}[2]{\left\langle #1\,,\, #2 \right\rangle_F}
''')
        eqanimate(self, *info)
~~~

Where 

- the class and method structure is for manim
- the first parameter of `eq` is the main content with latex + comments to show colored groups
- the second parameter of `eq` is optional and is used here to define custom commands
- `eqanimate` registers the manim animations

It can be run with the manim command `manim -pql test-eqcolor.py` which previews and sets the quality to low.

## Some helpers

Some commands

~~~bash
#P=media/videos/test-eqcolor/1080p60/partial_movie_files/Example
P=media/videos/test-eqcolor/480p15/partial_movie_files/Example
vids() {
    cat $P/*.txt | sed -e 1d -e "s@file 'file:$(pwd)/@@g" -e 's@.$@@g'
}
prestpl() {
    python3 -m manim_eqcolor.pres_tpl
}
~~~

Viewing the videos by chunk

~~~bash
xplayer $(vids)
~~~

Generating a simple html pres with videos (experimental)

~~~bash
(prestpl | awk '{print} $0 == "<!--HERE-->" {exit}' ; vids | while read i ; do echo "<video src='$i'></video>" ; done ; prestpl | awk 'go {print} $0 == "<!--HERE-->" {go=1}') > pres.html

firefox pres.html
~~~

Generating a more complex pres with reverse videos also (experimental)

~~~bash
for i in $(vids) ; do ffmpeg -y -i "$i" -vf reverse "$i-rev.mp4" ; done

(prestpl | awk '{print} $0 == "<!--HERE-->" {exit}' ; vids | while read i ; do echo "<div><video src='$i'></video><video src='$i-rev.mp4'></video></div>" ; done ; prestpl | awk 'go {print} $0 == "<!--HERE-->" {go=1}') > pres.html 

firefox pres.html
~~~
