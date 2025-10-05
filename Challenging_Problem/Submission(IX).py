import numpy as np
import random
import math
import matplotlib.pyplot as plt
from scipy.io import savemat
import os
from skimage import data
from skimage.color import gray2rgb

# -------------------- SETTINGS --------------------
OUTPUT_DIR = r"C:\Users\shiva\Documents\Ai_Lab_Report_MidSem\Challenging_Problem"
MAT_FILE = os.path.join(OUTPUT_DIR, "scrambled_lena.mat")
R, C = 4, 4                  # number of rows and columns of tiles
INIT_T, FINAL_T, COOL = 5.0, 1e-3, 0.995
MAX_ITER, SWEEP, SAVE_PERIOD = 50000, 200, 5000
# --------------------------------------------------

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------- IMAGE GENERATION --------------------
def create_test_image():
    """Load Lena image and convert to RGB float32."""
    img = data.astronaut()  # Use astronaut image as test
    img = img.astype(np.float32) / 255.0
    return img

def tile_img(img, R, C):
    h, w = img.shape[:2]
    th, tw = h // R, w // C
    tiles = [img[r*th:(r+1)*th, c*tw:(c+1)*tw] for r in range(R) for c in range(C)]
    return tiles, (th, tw)

def scramble_tiles(tiles):
    perm = list(range(len(tiles)))
    random.shuffle(perm)
    scrambled = [tiles[i] for i in perm]
    return scrambled, perm

def save_mat(tiles, filename):
    """Save tiles in .mat file."""
    mat_dict = {"tiles": np.array(tiles)}
    savemat(filename, mat_dict)

# -------------------- SA RECONSTRUCTION --------------------
def build_img(tiles, perm, R, C, shape):
    th, tw = shape
    out = np.zeros((R*th, C*tw, 3), dtype=np.float32)
    for i, t in enumerate(perm):
        r, c = divmod(i, C)
        out[r*th:(r+1)*th, c*tw:(c+1)*tw] = tiles[t]
    return out

def border_mse(a, b, side):
    if side == 'r':
        diff = a[:, -1] - b[:, 0]
    else:
        diff = a[-1] - b[0]
    return np.mean(diff**2)

def cost(tiles, perm, R, C):
    s = 0
    for i in range(R*C):
        r, c = divmod(i, C)
        if c < C-1:
            s += border_mse(tiles[perm[i]], tiles[perm[i+1]], 'r')
        if r < R-1:
            s += border_mse(tiles[perm[i]], tiles[perm[i+C]], 'd')
    return s

def simulated_annealing(tiles, R, C):
    N = R * C
    perm = list(range(N))
    random.shuffle(perm)
    cur_cost = cost(tiles, perm, R, C)
    best_cost, best_perm = cur_cost, perm.copy()
    T, iteration = INIT_T, 0

    while T > FINAL_T and iteration < MAX_ITER:
        for _ in range(SWEEP):
            i, j = random.sample(range(N), 2)
            perm[i], perm[j] = perm[j], perm[i]
            new_cost = cost(tiles, perm, R, C)
            if new_cost < cur_cost or random.random() < math.exp((cur_cost - new_cost)/T):
                cur_cost = new_cost
                if cur_cost < best_cost:
                    best_cost, best_perm = cur_cost, perm.copy()
            else:
                perm[i], perm[j] = perm[j], perm[i]  # revert swap
            iteration += 1

            if iteration % SAVE_PERIOD == 0:
                img_out = build_img(tiles, best_perm, R, C, tiles[0].shape[:2])
                plt.imsave(os.path.join(OUTPUT_DIR, f"sa_out_{iteration}.png"), np.clip(img_out, 0, 1))

        T *= COOL

    return best_perm, best_cost

# -------------------- MAIN --------------------
if __name__ == "__main__":
    print("Creating test image...")
    img = create_test_image()

    print("Tiling image...")
    tiles, shape = tile_img(img, R, C)

    print("Scrambling tiles and saving as .mat...")
    scrambled_tiles, perm = scramble_tiles(tiles)
    save_mat(scrambled_tiles, MAT_FILE)
    print(f"Saved scrambled tiles to {MAT_FILE}")

    print("Running Simulated Annealing...")
    best_perm, best_cost = simulated_annealing(scrambled_tiles, R, C)

    print("Building final reconstructed image...")
    final_img = build_img(scrambled_tiles, best_perm, R, C, shape)
    final_path = os.path.join(OUTPUT_DIR, "sa_final.png")
    plt.imsave(final_path, np.clip(final_img, 0, 1))
    print(f"Saved final image at {final_path}")

    plt.imshow(final_img)
    plt.axis("off")
    plt.show()
