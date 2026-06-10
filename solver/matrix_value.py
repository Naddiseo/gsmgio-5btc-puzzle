"""VALIDATED: the 'matrix' in the 2023-02-23 recipe slot `matrixsumlist`.

It is the phase-0 image grid read as a 196-bit binary number (W/Y=0, K/U=1) in
the same counter-clockwise spiral that decodes the URL, with the 4 centre
(bunny) squares zeroed -- the creator's "four zeros were omitted from the matrix".

This independently reproduces the number the community derived
(40585734329412479690520338541901772425587069158131163878976).
"""
import numpy as np
from PIL import Image
import os

MATRIX_NUMBER = 40585734329412479690520338541901772425587069158131163878976

def compute(png="puzzle.png"):
    here = os.path.dirname(os.path.abspath(__file__))
    for c in (png, os.path.join(here, "..", png)):
        if os.path.exists(c):
            png = c
            break
    im = np.array(Image.open(png).convert("RGB")).astype(int)
    G = im[:1047, :1048]
    N = 14
    ch, cw = G.shape[0] / N, G.shape[1] / N

    def cl(px):
        r, g, b = px
        if r > 140 and g > 140 and b < 130: return 'Y'
        if b > 120 and b - r > 40 and b - g > 40: return 'U'
        if r < 100 and g < 100 and b < 100: return 'K'
        if r > 150 and g > 150 and b > 150: return 'W'
        return '?'

    grid = [[cl(np.median(G[int((r + .5) * ch) - 12:int((r + .5) * ch) + 12,
                            int((c + .5) * cw) - 12:int((c + .5) * cw) + 12].reshape(-1, 3), axis=0))
             for c in range(N)] for r in range(N)]
    t, b, l, r = 0, N - 1, 0, N - 1
    order = []
    while t <= b and l <= r:
        for i in range(t, b + 1): order.append((i, l))
        for j in range(l + 1, r + 1): order.append((b, j))
        for i in range(b - 1, t - 1, -1): order.append((i, r))
        for j in range(r - 1, l, -1): order.append((t, j))
        t += 1; b -= 1; l += 1; r -= 1
    bits = ['0' if grid[r][c] in ('W', 'Y') else '1' for r, c in order]
    for i in range(len(bits) - 4, len(bits)): bits[i] = '0'  # zero the 4 bunny squares
    return int(''.join(bits), 2)

if __name__ == "__main__":
    v = compute()
    print("computed:", v)
    print("matches known:", v == MATRIX_NUMBER)
