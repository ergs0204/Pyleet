class Solution:
    def isValid(self, s: str) -> bool:
        if len(s)%2==1:
            return False
        stack=[]
        pair={"(":")","[":"]","{":"}"}
        for chr in s:
            if chr in pair:
                stack.append(chr)
            else:
                if not stack or chr!=pair[stack[-1]]:
                    return False
                stack.pop()
        return len(stack)==0