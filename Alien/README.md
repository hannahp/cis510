=============
Claw Machine 
===============
Final Project for CIS 510
Author: Hannah P.

A remote interface for a physics simulation of a claw machine.
 
======================================
Instructions for using Qt Interface
======================================
1. Start MayaPyApplication
2. Open "hannahPFinalProject.ma" in Maya (resources/mayaProj/clawMach/hannahPFinalProject.ma)
3. Turn on Nimble Server in Maya
4. Enter a number in the spin box and click "Spawn Aliens"*
5. "Key claw position" will key the Z and X of the claw at the current time in the Maya GUI. Move the claw where you like along the timeline*
6. Click "Drop Claw" to key the entire 3-second claw animation
7. Back in the Maya GUI, move to the time you want the claw to release
8. Click "Release claw"

* (Steps 4 and 5 can be reversed in order, if desired. 
Moving the claw/scrubbing the timeline with all the active aliens in place will slow down Maya significantly. 
Just be sure to spawn aliens BEFORE dropping the claw.)

=====================================
!!!!!!!!!!!!!!!!!---IMPORTANT NOTES---!!!!!!!!!!!!!!!!!!!!
=======================================

IMPORTANT NOTE #1: The alien in the scene when first opened is NOT rigged to have a gravity field.
This is because duplicating the object's input connections with gravity displays weird behavior.
Therefore, the "Spawn Aliens" button duplicates the initial alien, then hooks ALL of them to a
gravity field. 

Attempting to pick up the first alien without spawning others will not work properly. The claw will go through the alien, as it is not rigid yet.

Similarly, hitting "spawn aliens" a second time will not work properly, since the 
template alien will have been connected to gravity already. If I had more time, I would fix this.

IMPORTANT NOTE #2: 
I am not sure if it is just my install of Maya, or something with my ma file, but randomly
the "autosave" prompt from the student version will come up and then Maya will freeze. I have
turned off Autosave for a long time to prevent this; however, the auto-save prompt still comes up on occasion and
causes freezing.