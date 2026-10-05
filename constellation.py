n = int(input().strip()
s = list(map(int, n))
if s[0] == s[1] == s [2] == s[3]:
    print("MASTER")
elif s[0] == s[3] and s[1] == s[2]:
    print("MIRROR")
elif (s[1] == s[0] + 1 and s[2] == s[1] + 1 and s[3] == s[2] + 1) or \
     (s[1] == s[0] - 1 and s[2] == s[1] - 1 and s[3] == s[2] - 1):
    print("LADDER")
elif s[0]==s[1] or s[1]==s[2] == s[3]:
    print("TWIN")
else:
    print("REJECT")