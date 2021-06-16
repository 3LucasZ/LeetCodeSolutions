class Solution:
    def phraseMatch(self, s, p):
        if len(s) != len(p):
            return False

        for i in range(len(s)):
            if(s[i] != p[i] and p[i] != "?"):
                return False
        return True
        
    def isMatch(self, s: str, p: str) -> bool:
        psplit = p.split("*")

        if len(psplit) == 1:
            return self.phraseMatch(s,p)

        else:
            #deal with the head and tail first
            if len(s) >= len (psplit[0]):
                if self.phraseMatch(s[0:len(psplit[0])], psplit[0]):
                    s = s[len(psplit[0]):]
                    psplit = psplit[1:]
                    if len(s) >= len (psplit[-1]):
                        if self.phraseMatch(s[len(s)-len(psplit[-1]):len(s)], psplit[-1]):
                            s = s[0:len(s)-len(psplit[-1])]
                            psplit = psplit[0:-1]
                        else:
                            print("tail does not match last phrase")
                            return False
                    else:
                        print("tail too short")
                        return False
                else:
                    print("head does not match first phrase")
                    return False
            else:
                print("head is too short")
                return False
            
        #everything good so far?
        print(s)
        print(psplit)

        #make sure we have the consecutive phrases
        k = 0
        while k < len(psplit):
            if len(s) < len(psplit[k]):
                print("s can not contain psplit[k]")
                return False
            
            if self.phraseMatch(s[0:len(psplit[k])], psplit[k]):
                s = s[len(psplit[k]):]
                k += 1
            else:
                s = s[1:]

        return True
#tests      
s = 'helloworld'
p = '*e?l*or*d'
dig = Solution()
print(dig.isMatch(s,p))
