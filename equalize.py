import cv2
import sys
from histogram_equalization import block_histogram_equalization, global_histogram_equalization
from getopt import getopt


def equalize_img():
    # Use getopt to gather our arguments
    img_name = None
    result_path = None
    block_size = 0

    opts, args = getopt(sys.argv[1:], "s:b:i:")
    for opt, arg in opts:
        if opt == "-b":
            block_size = int(arg)
        elif opt == "-s":
            result_path = arg
        elif opt == "-i":
            img_name = arg

    # Determine if global or block histogram equalization is occcuring and
    # proccess the image
    img = cv2.imread(img_name)
    if img is None:
        print("Image Error!")
        return

    if block_size == 0:
        equalized_img = global_histogram_equalization(img)
    else:
        equalized_img = block_histogram_equalization(
            img,
            (block_size, block_size))

    # If necessary, save the resulting image
    if result_path is not None:
        cv2.imwrite(result_path, equalized_img)

    # Display the resulting image at a quarter of its size
    cv2.imshow("Equalized Image", cv2.resize(
        equalized_img,
        (int(img.shape[1] * 0.25), int(img.shape[0] * 0.25))))
    cv2.imshow("Original Image", cv2.resize(
        img,
        (int(img.shape[1] * 0.25), int(img.shape[0] * 0.25))))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    equalize_img()
