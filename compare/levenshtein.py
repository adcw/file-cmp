def levenshtein(s1: str, s2: str):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j  # If s1 is empty, insert all characters of s2
            elif j == 0:
                dp[i][j] = i  # If s2 is empty, insert all characters of s1
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Characters are the same, no cost
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # Deletion
                    dp[i][j - 1],  # Insertion
                    dp[i - 1][j - 1]  # Substitution
                )
    return dp[m][n]


def levenshtein_norm(s1: str, s2: str):
    return 1 - levenshtein(s1, s2) / max(len(s1), len(s2))


if __name__ == '__main__':
    print(levenshtein_norm("abc", "abd"))
    print(levenshtein_norm("abc", "abc"))
