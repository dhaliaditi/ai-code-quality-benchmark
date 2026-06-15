
def is_nested(string):
    '''
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.

    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
    '''
    opening = [i for i, ch in enumerate(string) if ch == '[']
    closing = [i for i, ch in enumerate(string) if ch == ']']
    closing.reverse()
    count = 0
    j = 0
    for i in opening:
        if j < len(closing) and i < closing[j]:
            count += 1
            j += 1
    return count >= 2
