# CK3-death-emu
Emulate natural death in crusader kings III with python script.

Thanks @Frigabus for offering the formula. 
You can find the original excel at https://forum.paradoxplaza.com/forum/threads/help-understanding-health-age-and-death.1427437/

I think that if each month the death rate is $p$, for a year it should be $1-(1-p)^12$ rather than $12p$, so my formula is a little different.
It's better to generate random numbers for each month, but there won't be much difference.
