import cv2
import os


class Cartoonify:
    def cartoonify(self, image_path):
        # create a temporary image path for it to be displayed in the UI.
        image_dir = os.path.dirname(image_path)
        image_filename = os.path.basename(image_path)
        image_name, image_extension = os.path.splitext(image_filename)
        temp_image_path = os.path.join(image_dir, "{}_temp{}".format(image_name, image_extension))

        # read the image
        original_image = cv2.imread(image_path)
        # convert the image to grayscale
        grayscale_im = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        # smoothen the image
        smooth_gs_im = cv2.medianBlur(grayscale_im, 5)
        # get the edges of the image using adaptive threshold
        edge_img = cv2.adaptiveThreshold(smooth_gs_im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        # sharpen the image
        color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
        # combine the two images using bitwise AND operation.
        cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edge_img)
        resized_modified_image = cv2.resize(cartoon_image, (960, 540))
        # save the temporary image
        cv2.imwrite(temp_image_path, resized_modified_image)
        return temp_image_path


