import sys
from scipy.stats import f

def FisherTest(RSS_1, RSS_2, dof_1, dof_2, N):
    RSS1 = float(RSS_1)
    RSS2 = float(RSS_2)
    n1 = N - dof_1 - 1
    n2 = N - dof_2 - 1
    print("n1 = {0}    n2 = {1}".format(n1, n2))
    F = abs(((RSS1 - RSS2) / (n2 - n1)) / (RSS2 / (N - n2)))
    print("d1 = {0}    d2 = {1}".format(n2-n1, N-n2))

    # Calculating the p-value
    p_value = 1 - f.cdf(F, n2 - n1, N - n2)

    return F, p_value

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python FisherTest.py RSS1 RSS2 DOF1 DOF2 N")
        sys.exit(1)

    RSS1, RSS2, DOF1, DOF2, N = sys.argv[1:6]
    F, p_value = FisherTest(RSS1, RSS2, int(DOF1), int(DOF2), int(N))
    print("F-value: {0:.2f}, P-Value: {1:.2f}%".format(F, p_value*100))
