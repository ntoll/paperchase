Paper Chase
===========

A very simple game written for `Pyweek 25 <https://pyweek.org/25/>`_
(installation instructions at the end).
`Read my developer diary for the event online <https://pyweek.org/e/ntoll/>`_.
The theme for this iteration of PyWeek is "Two Worlds".
In this instance the two worlds are the intergalactic rivals from the worlds of
the red biros vs the blue biros (there's a HHGG reference in there somewhere).
;-)

As the blurb from the start of the game says:

    "The intergalactic war between the red and blue factions of the biro
    universe has reached its climax. Each world has sent a stick-figure
    champion to race in the "Paper chase" for ultimate victory and to decide
    which colour biro pen teachers should use when marking work."

This is a two-player side-scrolling chase / avoidance game. **You win by
getting 200 steps ahead of the other player**.

As the figures run across the paper they encounter various obstacles which, if
hit, will slow the player down. If you snaffle a Python power-up (to import
antigravity) you'll be able to gain speed by flying.

The keys are:

 Action    Red     Blue
======== ======= ========
   Up      Up       W
  Down    Down      S
  Kick    Right     d
  Jump    Enter    Space
======== ======= ========

As the game progresses the obstacles come more often and the pace of the
game speeds up.

The wider point of the game is educational:

* I'm using Dan Pope's amazing PyGame Zero and writing the code using the Mu
  editor.
* I aim to create a game that is simple enough that it could be used as a
  "template" or launch pad for teachers and beginner programmers who want to
  write their own games.
* The game will be a single logic file and single data file.
* The game assets will be generated in as simple a manner as possible (i.e.
  something kids could easily copy).
* Post-PyWeek I'm going to write this all up into an educational resource.

Running the Game
================

**PaperChase only works with Python 3!**

I've tested the game works on Windows 10 (64bit), OSX (High Sierra) and Ubuntu
Linux (17.10).

Installation is relatively simple::

    $ pip3 install pgzero

Installing PyGame Zero will bring down PyGame and other associated
requirements.

**NOTE: As of time of writing, PyGame Zero has a misconfiguration issue in OSX
which means that keyboard capture doesn't work if you're running the game
within a virtualenv. In this case, just use the system Python 3 and ``pip
install pgzero`` globally (sorry).**

Simply change directories into the root of the project (i.e.
the directory in which you'll find this file) and type::

    $ pgzrun paper_chase.py

...and grab a friend for the battle of the biroid champions.

Most of all, I hope you have as much fun playing it as I did writing it!
