import cv2
import numpy as np
from math import floor

def compute_cdf(histogram, img_dim):
    cdf = np.copy(histogram)

    cdf = np.cumsum(cdf)
    cdf = cdf / (img_dim[0] * img_dim[1])

    return cdf


def compute_hist_equalizer(img):
    hist_blue = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_green = cv2.calcHist([img], [1], None, [256], [0, 256])
    hist_red = cv2.calcHist([img], [2], None, [256], [0, 256])

    blue_equalizer = compute_cdf(hist_blue, img.shape)
    green_equalizer = compute_cdf(hist_green, img.shape)
    red_equalizer = compute_cdf(hist_red, img.shape)

    repeated_255 = np.repeat(255, 256)
    blue_lookup = blue_equalizer * repeated_255
    green_lookup = green_equalizer * repeated_255
    red_lookup = red_equalizer * repeated_255

    return np.dstack((blue_lookup, green_lookup, red_lookup)).astype(np.uint8)


def gather_block_equalizers(img, block_size):
    block_lookups = []

    for i in range(0, img.shape[0], block_size[0]):
        lookups_row = []
        for j in range(0, img.shape[1], block_size[1]):
            img_block = img[i:i+block_size[0], j:j+block_size[1]]
            lookups_row.append(compute_hist_equalizer(img_block))

        block_lookups.append(lookups_row)

    return block_lookups


def block_histogram_equalization(img, block_div):
    block_size = (
        int(img.shape[0]/block_div[0]),
        int(img.shape[1]/block_div[1]))

    img = img.copy()
    block_equalizers = gather_block_equalizers(img, block_size)
    for i in range(0, block_div[0]):
        for j in range(0, block_div[1]):
            img_block = img[
                i*block_size[0]:(i+1)*block_size[0],
                j*block_size[1]:(j+1)*block_size[1]]
            equalized_block = cv2.LUT(img_block, block_equalizers[i][j])

            img[
                i*block_size[0]:(i+1)*block_size[0],
                j*block_size[1]:(j+1)*block_size[1]] = equalized_block

    return img


def global_histogram_equalization(img):
    hist_blue = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_green = cv2.calcHist([img], [1], None, [256], [0, 256])
    hist_red = cv2.calcHist([img], [2], None, [256], [0, 256])

    blue_equalizer = compute_cdf(hist_blue, img.shape)
    green_equalizer = compute_cdf(hist_green, img.shape)
    red_equalizer = compute_cdf(hist_red, img.shape)

    repeated_255 = np.repeat(255, 256)
    blue_lookup = np.ndarray.flatten(blue_equalizer) * repeated_255
    green_lookup = np.ndarray.flatten(green_equalizer) * repeated_255
    red_lookup = np.ndarray.flatten(red_equalizer) * repeated_255

    lookup = np.dstack((
        blue_lookup,
        green_lookup,
        red_lookup
    )).astype(np.uint8)

    return cv2.LUT(img, lookup)