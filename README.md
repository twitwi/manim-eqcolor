

## Non-minimal Example (quick doc)

In a file (e.g., `test-eqcolor.py`), we put

~~~python3
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

Packing in folder (with reverse mp4 already generated (see above)).

~~~bash
echo "enter output folder name (to create)"
read F
mkdir "$F"

for i in $(vids) ; do cp -t "$F" "$i" "$i-rev.mp4" ; done
(prestpl | awk '{print} $0 == "<!--HERE-->" {exit}' ; vids | while read i ; do i=$(basename "$i"); echo "<div><video src='$i'></video><video src='$i-rev.mp4'></video></div>" ; done ; prestpl | awk 'go {print} $0 == "<!--HERE-->" {go=1}') > "$F/index.html"

echo firefox "$F/index.html"
~~~


Same but ignoring shorter (pure wait, by convention)

~~~bash

(prestpl | awk '{print} $0 == "<!--HERE-->" {exit}' ; vids | while read i ; do duration=$(ffprobe -i "$i" -show_entries format=duration -v quiet | grep duration | sed 's@.*=@@g') ; if (( $(echo "$duration > 0.5" | bc -l) )) ; then cp -t "$F" "$i" "$i-rev.mp4" ; i=$(basename "$i"); echo "<div><video src='$i'></video><video src='$i-rev.mp4'></video></div>" ; fi ; done ; prestpl | awk 'go {print} $0 == "<!--HERE-->" {go=1}') > "$F/index.html"

#for i in $(vids) ; do duration=$(ffprobe -i "$i" -show_entries format=duration -v quiet | grep duration | sed 's@.*=@@g') ; if (( $(echo "$duration > 0.5" | bc -l) )) ; then cp -t "$F" "$i" "$i-rev.mp4" ; fi ; done
~~~
