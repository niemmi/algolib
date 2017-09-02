"""Finds the longest palindromic substring in O(n) time using Manacher's
algorithm. Algorithm is based on the observation that if sub-palindrome fully
contained within left half of larger palindrome ends exactly to the left
boundary of longer boundary only then the mirror sub-palindrome on the right
side might be longer.

  s s s
  l l l l l
d b a b a b c . . .
1 1 3 5
0 1 2 3 4 5

In above string 'abbbbbc...' has been examined until index 3 and palindrome
lengths have been tracked now. Since longest palindrome centered at index 2
ends the same place as longest palindrome centered at index 3 we know that
palindrome centered at 4 is _at least_ 3 characters long and in order to
discover the full length we can start comparing from locations 2 and 6.

  s s s
  l l l l l
x a x b x a c . . .
1 3 1 5
0 1 2 3 4 5 6

In above we know that longest palindrome in index 4 is 1 since the mirror
palindrome centered at 2 has the same length -> we can just write down length
1 at index 4 and move to index 5. At index 5 we check mirror index 1 which is 3.
Since that palindrome goes outside of bounds of longer palindrome centered at
3 we can just mark down 1 + 2 * length to boundary of longer palindrome -> 1.
Note that if there would be a palindrome of length 3 centered at 5 we would have
noticed that when expanding boundaries for longer palindrome centered at 3 since
in that case indexes 0 & 6 must have matched.

Next we move to index 6 which lies outside of boundaries of the longer
palindrome thus we need to start matching to see if there's a palindrome of
length of 3.

Above pays zero consideration to palindromes with even length. We can easily
modify the input string to have boundary characters before and after the string
and between every character:

| x | a | x | b | x | a | c |
1 3 1 7 1 2 1 11
0 1 2 3 4 5 6 7

Note that we can also prefill the auxiliary length array with 1s & 3s since
every letter can be matched with boundary markers surrounding it. The other
adjustment is dividing the maximum palindrome length by 2 before returning it.
"""


def longest_palindromic_substring(s):
    """Finds longest palindromic substring.

    Args:
        s: String to search the palindrome from.

    Returns:
        Length of longest palindrome.
    """
    if not s:
        return 0

    # Make sure the palindromes are of odd length by adding divider at
    # the ends and between every character
    s = '|' + '|'.join(s) + '|'
    n = len(s)

    # Fill the match length for each palindrome center, notice that if l[x]
    # contains letter we know that we can match dividers on both sides
    lengths = [1 + 2 * (i % 2) for i in range(n)]
    center = 2

    while center < n:
        # Match around current center as far as we can, O(n) time complexity
        # comes from the fact that we only have to start matching from where
        # we stopped last time since l[c] might be > 1 (or 3)
        i = lengths[center] // 2 + 1
        while (center - i >= 0 and center + i < n
               and s[center - i] == s[center + i]):
            i += 1

        # Walk forward of current center, and update until we either hit
        # a place where mirror location on the left ends exactly at
        # the boundary of center or we run out of examined area.
        # Where ever we will stop will be the new center
        lengths[center] = i * 2 - 1
        for j in range(1, i):
            limit = (i - j) * 2 - 1

            # Limit the match length to left boundary
            lengths[center + j] = min(limit, lengths[center - j])

            # Stop if mirror match ends exactly at the boundary
            if lengths[center - j] == limit:
                center += j
                break
        else:
            # Run out of matched area
            center += i

    return max(lengths) // 2
