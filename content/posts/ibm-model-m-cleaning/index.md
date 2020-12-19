---
author: Nathan Vaughn
cover: img/model-m-angle.jpg
date: "2020-12-18"
description: Cleaning an original IBM Model M from 1986
images:
- /posts/ibm-model-m-cleaning/img/model-m-angle.jpg
tags:
- IBM
- Model M
- mechanical keyboards
title: "IBM Model M cleaning"
userelativecover: true
---

## Background

As a graduation gift, a friend gave me an IBM Model M keyboard that he snagged
from the university surplus store
(not the [first time]({{< relref "sun-ultra-24-build" >}}) that the surplus
store has made an appearance with vintage tech).

{{< figure src="img/model-m-main.jpg" alt="1986 IBM Model M" caption="1986 IBM Model M" >}}

This keyboard is absolutely delightful, and I wanted to make a post outlining
my process of cleaning the board.

## IBM Model M History

First, a history lesson.

The year is 1981. IBM has just released the first IBM Personal Computer.
With each IBM PC came a [buckling spring](https://en.wikipedia.org/wiki/Buckling_spring)
IBM Model F keyboard. Now, the standard keyboard
layout we know today has not been developed yet. These Model F keyboards,
while well-built and pleasant to type on, had a strange layout (by today's standards).

{{< figure src="img/model-f-wiki.png" alt="1984 IBM Model F" caption="1984 IBM Model F" >}}

The function keys were in columns on the left side and the numpad had a weird layout
with no addition or division keys. While the IBM PC was revolutionary for its time,
IBM realized it could develop a more ergonomic keyboard, and sought out to improve
their Model F. Hence, in 1984, the IBM Model M was born.

The IBM Model M (also known as the "IBM Enhanced Keyboard") is the grandfather of
all modern keyboards.

{{< figure src="img/model-m-wiki.png" alt="1986 IBM Model M" caption="1986 IBM Model M" >}}

With what IBM learned from their ergonomics studies in the years
prior, they moved the function keys to be above the number keys, in groups of four.
They also rearranged the numpad, added the arrow keys, and added the six key block
of <kbd>Insert</kbd>, <kbd>Home</kbd>, <kbd>Delete</kbd>, <kbd>End</kbd>, <kbd>Page Up</kbd>, and <kbd>Page Down</kbd> keys. However, they refused
to add the increasingly common <kbd>⊞ Win</kbd> key to their keyboard, opting to leave a blank
space on either side of the Alt keys instead.

Now, in order to reduce costs from the Model F,
IBM made some compromises with the Model M. Primarily, these were to change the
Model F's design with a capacitive membrane and full
[N-key rollover](https://en.wikipedia.org/wiki/N-key_rollover), to a
membrane design and losing the N-key rollover support.

The history of the Model M is long and complicated as well over
[100 different variants](https://en.wikipedia.org/wiki/Model_M_keyboard#Features_by_part_number)
were produced (different colors, keyboard layouts, design improvements,
connectors, logo style, etc.). The short version is that in 1991, IBM decided
it didn't want to continue manufacturing keyboards, and sold its keyboard business
to Lexmark. Lexmark continuing making Model Ms until 1996 when they stopped production.
After this, a group of ex-Lexmark employees bought the rights
and manufacturing tooling, and formed the company
[Unicomp](https://www.pckeyboard.com/), who continues to manufacture
brand-new Model M's to this day in different colors, with Windows keys, and USB support
(just without the IBM branding).

{{< figure src="img/model-m-unicomp.jpg" alt="A new Unicomp Model M" caption="A new Unicomp Model M"  >}}

Over the years, to decrease manufacturing costs, the Model M's were made cheaper
by using lower quality plastics, and thinner components. This means that generally, the
older a Model M is, the better built it is. This unfortunately means that Unicomp
keyboards, while as close to real thing as you can get new, are based off the molds
and manufacturing at the end of production, resulting in the lowest-quality of
the Model M series.

{{< figure src="img/model-m-gens.jpg" alt="Table of the Model M generational differences" caption="Table of the generational differences of the Model Ms from [Chyrosran22's fantastic video](https://youtu.be/r5H58uudo1Y?t=545)." >}}

## My Specific Keyboard

With all that out of the way, let's look at the exact keyboard I have.

{{< figure src="img/birth-certificate.jpg" alt="My IBM Model M's birth certificate" caption="My IBM Model M's birth certificate"  >}}

My Model M is a part number 1390120 and was built on January 14, 1986. There's a few
notable features about this part number compared to most.

{{< figure src="img/tramp-stamp.jpg" alt="My Model M has no lock lights and a square badge" caption="My Model M has no lock lights and a square badge"  >}}

Two of the most notable things are that

1. There are no lock lights
2. It has a square IBM badge

This tells us that the keyboard was one of the original generations produced, as
the square IBM badges were only made for a few years before being replaced
by oval badges. Additionally, the keyboard has no lock lights. This means that it must
have been bundled with a PC or terminal that displayed the lock light status on
the monitor rather than keyboard.

There are two more things that stand out to me. First, is the connector.

{{< figure src="img/sdl-connector.jpg" alt="Removable SDL connector on the keyboard" caption="Removable SDL connector on the keyboard"  >}}

This keyboard has a removable
[SDL](https://en.wikipedia.org/wiki/Shielded_data_link_connector) connector. As this
keyboard actually predates the [PS/2 protocol](https://en.wikipedia.org/wiki/PS/2_port)
by a year, this keyboard likely came with a SDL to
[AT](https://deskthority.net/wiki/AT_keyboard_interface)
(basically a 5-pin DIN connector) cable from the factory.

{{< figure src="img/sdl-cable.jpg" alt="SDL to PS/2 cable given to me" caption="SDL to PS/2 cable given to me"  >}}

However, the keyboard was still compatible with the PS/2 protocol once
it had been developed. While the original cable for the keyboard is long-gone, with
the keyboard itself, I was given a SDL to PS/2 cable that works perfectly fine on modern
motherboards.

{{< figure src="img/relegendable.jpg" alt="Relegendable keycaps" caption="Relegendable keycaps. Here, I've pulled off the top keycaps with the legends from the arrow keys."  >}}

Lastly, this keyboard also features relegendable keycaps. The keycap on each key is
actually two pieces. The top piece comes off fairly easily with just your fingers,
while the bottom piece is more firmly attached to the spring of each switch. This
was done to make different localizations of the keyboards easier, as the keyboards
and bottom keycaps could be mass produced, and only a secondary top keycap set
produced for each localization.

{{< figure src="img/side-legends.jpg" alt="Keycap side legends" caption="Interestingly, some keycaps have side legends, and some in different colors. The colors got removed from later models, but I find these interesting as not many keyboards have this today." >}}

## Cleaning

Let's get [down to business](https://youtu.be/TVcLIfSC4OE). This keyboard had
almost 35 years of grime on it. It wasn't *bad* considering its age,
but it wasn't *good* either.

{{< figure src="img/grime.jpg" alt="Keyboard grime" caption="30+ years in an academic environment has left its residue"  >}}

To clean my Model M I used the following tools:

{{< figure src="img/cleaning-tools.jpg" alt="Tools needed for cleaning" caption="Tools needed for cleaning"  >}}

- [Keycap puller](https://www.maxkeyboard.com/max-wire-key-cap-puller-tool.html)
- [5.5mm nut driver](https://www.amazon.com/gp/product/B000BQ4XP6)
- Flat-head screwdriver
- Tweezers
- Isopropyl alcohol
- Lots of paper towels
- Small bin

The nut driver was a real pain. The 4 bolts required to disassemble the Model M
are 7/32". My universal socket set was too wide to fit into the recesses to actually
reach the head of each bolt. Finding an individual 7/32" nut driver online was
expensive so I ended up ordering the linked 5.5mm nut driver for cheap instead.
The sizes are nearly identical and it works fine.

First, flip the keyboard upside down and remove these 4 bolts with your nut driver.

{{< figure src="img/bolt-removal.jpg" alt="Removing the 4 primary bolts" caption="Removing the 4 primary bolts" >}}

After you've done that, flip the keyboard right side up, and remove the top shell.
It should unsnap pretty easily.

{{< figure src="img/top-shell-removed.jpg" alt="Top shell removed" caption="Top shell removed" >}}

With the top shell taken off, I could see how dirty the keyboard really was.

{{< figure src="img/under-grime.jpg" alt="Grime under the top shell" caption="All the grime the top shell was hiding" >}}

Before the backplate can be removed, you first need to undo a small grounding
strap located in the top left of the keyboard. This is held on by a flat-head bolt
with a washer and a nut.

{{< figure src="img/grounding-strap.jpg" alt="Grounding strap disconnection" caption="Remove the bolt holding the grounding strap" >}}

Before you can take out the backplate, there are two ribbon cables connecting
the keyboard's controller. I found the ribbon cables in my keyboard
were pretty well attached, so I disconnected them outside of the case.
Either way, you can lift out the backplate. Tilt it forwards to the front and lift
gently (especially if the controller is still connected). It might need a little
wiggle to free it.

{{< figure src="img/full-disassembly.jpg" alt="Keyboard fully disassembled" caption="Now all the major components are removed" >}}

Now is a good time to inspect the rivets on the backside of the backplate.
While the Model Ms were a great keyboard,
they had one major design flaw. To save cost, IBM used plastic rivets
to connect the steel backplate to the membrane and plastic housing for the switches.
Over time, these rivets tend to break from becoming brittle with age, and everyday
typing forces.

{{< figure src="img/broken-rivets.jpg" alt="Two broken plastic rivets" caption="Two plastic rivets pictured here have had their heads sheared off" >}}

If too many of these rivets are sheared off, you will
likely need to
[bolt](https://wiki.geekhack.org/index.php?title=Modifications:IBM_Model_M:Nut_and_Bolt_Mod)
[mod](https://deskthority.net/viewtopic.php?t=9169)
your keyboard to permanently replace the plastic rivets. In my case, only 4
were broken so I left it.

{{< figure src="img/rivet-head.jpg" alt="Broken plastic rivet head" caption="One of many plastic rivet heads found rattling around inside the keyboard" >}}

Also on the backside of the backplate are two inspection stickers from the factory.
Notice the absolutely gorgeous shiny rainbow finish of the backplate.

{{< figure src="img/serial-sticker.jpg" alt="Serial number sticker" caption="Serial number sticker. Curiously, the person who initialed it has the same initials as me." >}}

{{< figure src="img/qa-sticker.jpg" alt="QA sticker" caption="QA sticker" >}}

The controller PCB was very clean so I left it alone.

{{< figure src="img/pcb.jpg" alt="Three photos of the controller PCB" caption="Controller PCB pictures for anyone interested. You can see the connector on the right side of the board for a daughter board for the lock lights." >}}

### Shell

Now, time to clean the keyboard. For the two shell halves, I used isopropyl alcohol
along with soap to clean as much grime as I could off the surface of the plastic.
For some of the tough to reach areas like the grooves on the top shell,
I used a small flat-head screwdriver with the tip wrapped with some paper towels soaked
in alcohol, and ran it back and forth. Worked pretty well, though I may have
scraped a little bit of plastic off.

Now, there were some nicks on the upper shell. I decided to just leave them as-is.
I was afraid trying to sand them down at all would do more harm than good.

{{< figure src="img/nicks.jpg" alt="Nicks on the keyboard shell" caption="Just a few nicks on the edges of the shell" >}}

As for the Iowa State University tramp stamp on the top, I also decided to leave that.
After all, that's how I got the keyboard, the badge itself is in fine shape,
and it gives the keyboard a special uniqueness to it.

### Keycaps

To clean the keycaps, I first removed all the top layer keycaps and put them in small
tub.

{{< figure src="img/top-keycaps-removed.jpg" alt="All of the top keycaps removed" caption="This is after removing all the top keycaps. Note: I took this picture *after* cleaning. The keycap on the numpad <kbd>+</kbd> key should actually be on the stem for right <kbd>Ctrl</kbd>." >}}

Be careful when removing the spacebar, and numpad <kbd>+</kbd> and <kbd>Enter</bkd>
keys, as they have stabilizers. The stabilizers for the two numpad keys have a slight
bend in them as well that follows the curve of the keycap, so remember this
when putting the keycaps back on.

{{< figure src="img/stabilizier.jpg" alt="Numpad key stabilizer" caption="The stabilizer matches the curve of the keycap so it is directional" >}}

For all the keycaps in my tub, I filled it with warm soapy water and let them soak
for an hour.

{{< figure src="img/keycap-bath.jpg" alt="Keycaps soaking in soapy water" caption="" >}}

This doesn't hurt the legends at all as they are
[dye-sublimated](https://deskthority.net/wiki/Keycap_printing#Dye_sublimation).
The grime came right off with just a wipe of paper towel.

{{< figure src="img/dirty-keycap-bath.jpg" alt="Dirty keycap water after soaking" caption="This water was clean when I put the keycaps in" >}}

To reassemble, I found it easier to put the keycaps with stabilizer on the spring first,
then feed the stabilizer into its slot rather than the other way around.

### Baseplate

To clean the baseplate, I also took off all the bottom keycaps.

{{< figure src="img/bottom-keycaps-removed.jpg" alt="Bottom keycaps removed" caption="Bottom keycaps removed" >}}

I initially tried to clean the baseplate without removing these, as I knew getting
junk into the switch stems is very bad, but they're just too much in the way.
Just be careful to not drop anything down the switch stems.

Unlike most keyboards, you don't need to keep track of which row which keycap came from.
On a Model M, the profile of every keycap is identical. To achieve per-row sculpting,
the switches themselves are put on a curve.

{{< figure src="img/keycap-profiles.jpg" alt="Standard keycap profiles versus Model M keycap profiles" caption="Top: [SA profile keycaps](https://drop.com/buy/ascii-sa-pbt-dye-subbed-custom-keycap-set) on a straight keyboard. Bottom: Model M keycaps on its curved backplate." >}}

In terms of cleaning the backplate, I used a *lot* of paper towels soaked with alcohol.
To get in some of the tighter spaces, I again used a screwdriver tip wrapped in paper
towels to run through the spaces.

### Result

Reassembly is straightforward, just do everything in reverse.

I'm extremely pleased with the result. While not perfect, it's way better than
I originally got it, and looks absolutely magnificent.

{{< figure src="img/clean-1.jpg" alt="Picture of cleaned keyboard reassembled" caption="" >}}

{{< figure src="img/clean-2.jpg" alt="Closeup picture of cleaned keyboard reassembled" caption="This keyboard hasn't been this clean since it left the factory" >}}

## Review

Here's my thoughts on the keyboard. Mind you, I usually typed on Cherry MX Blues and
Browns prior. I don't have the time or money to be a true keyboard aficionado like
some on [/r/MechanicalKeyboards](https://www.reddit.com/r/MechanicalKeyboards).

{{< figure src="img/reddit-rant.jpg" alt="/u/SolitaryEgg has some strong feeling towards the /r/MechanicalKeyboards community" caption="/u/SolitaryEgg has some strong feeling towards the /r/MechanicalKeyboards community" >}}

### Feel

Overall, I like the board a lot. The tactileness of the switches is lovely, though
I usually bottom out keycaps anyways. The switches are far heavier than I was used to
with Blues and at first left my fingers feeling tired after lots of typing.

### Sound

The sound of the Model is definitely lower-pitched than Cherry switches, but a lot
more "pingy", which makes sense as the keys are directly connected to a spring.
I recorded samples of each for you to compare.

{{< figure src="img/audio-setup.jpg" alt="Microphone directly over my keyboard" caption="I got my mic as close as possible to the keyboard while leaving room for my hands" >}}

Each sample was done with no risers on the back deployed, and not modified in any way.

{{< audio src="audio/mxblues.mp3" caption="Cherry MX Blues" >}}

{{< audio src="audio/modelm.mp3" caption="Model M Buckling Springs" >}}

### Issues

There's a few things you have to deal with, with a keyboard this old.
First is the size. This thing is a ***monster***.
It's 19.25 inches long by 8.25 inches wide. It takes up a ton of desk space.

{{< figure src="img/desk-space.jpg" alt="Model M on my desk" caption="This thing consumes the majority of my [desk mat](https://bitwit.tech/shop/ensemble1-blupnk)" >}}

Additionally, the lack of Windows key can be problematic. I was able to get
around this by using the program [SharpKeys](https://github.com/randyrants/sharpkeys)
and remapping the [<kbd>Scroll Lock</kbd>](https://ux.stackexchange.com/a/64709) key
to act as a Windows key as I can't think of a time I've ever
actually needed the key.

Another thing is the PS/2 connector. While my motherboard does have a port, many
computers nowadays (especially laptops) do not, and PS/2 is also not hot-swappable
like USB. I went ahead bit the bullet and bought
[this $35 SDL to USB cable](https://ebay.us/oaGiIx)
that has an nice adapter built in to the cable itself. Unfortunately, it hasn't shown
up yet due to USPS delays, but it should make using the keyboard a bit easier and
more universal while not modifying the guts.

Lastly, with my specific keyboard not having any lock lights,
knowing whether <kbd>Num Lock</kbd> or <kbd>Caps Lock</kbd> is on can frustrating.
For this, I've found the program
[TrayStatus](https://www.traystatus.com/) works wonderfully for this,
by adding customizable icons in the Windows system tray.

{{< figure src="img/tray-lock-lights.jpg" alt="TrayStatus virtual lock lights on the far left"  caption="TrayStatus virtual lock lights on the far left" >}}

## Conclusion

I love this keyboard. It's loud, fun to type on, and built like a tank.
It's survived over 30 years in a university environment, and ready for 30 more.
While it may not be my daily driver, and too loud for office use, I fully plan on using
it frequently and  expect to be able to pass this down to my grandchildren.
They sure don't build 'em like they used to.

## References

- [https://www.youtube.com/watch?v=r5H58uudo1Y](https://www.youtube.com/watch?v=r5H58uudo1Y)
- [https://www.youtube.com/watch?v=D7wmMZmMinM](https://www.youtube.com/watch?v=D7wmMZmMinM)
- [https://en.wikipedia.org/wiki/Model_F_keyboard](https://en.wikipedia.org/wiki/Model_F_keyboard)
- [https://en.wikipedia.org/wiki/Model_M_keyboard](https://en.wikipedia.org/wiki/Model_M_keyboard)
- [https://en.wikipedia.org/wiki/Shielded_data_link_connector](https://en.wikipedia.org/wiki/Shielded_data_link_connector)
- [https://en.wikipedia.org/wiki/PS/2_port](https://en.wikipedia.org/wiki/PS/2_port)
- [https://deskthority.net/wiki/AT_keyboard_interface](https://deskthority.net/wiki/AT_keyboard_interface)
- [https://deskthority.net/wiki/Keycap_printing#Dye_sublimation](https://deskthority.net/wiki/Keycap_printing#Dye_sublimation)
- [https://www.reddit.com/r/MechanicalKeyboards/comments/d43o11/this_subreddit_in_a_nutshell/](https://www.reddit.com/r/MechanicalKeyboards/comments/d43o11/this_subreddit_in_a_nutshell/)
- [https://github.com/randyrants/sharpkeys](https://github.com/randyrants/sharpkeys)
- [https://www.traystatus.com/](https://www.traystatus.com/)
