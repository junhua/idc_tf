from PIL import Image,ImageOps,ImageDraw
import numpy as np
import glob
import random

def get_output_dir(input_dir, count=0):
    '''
    helper function to create output dir from input dir
    count var is to help naming the images
    '''

    filename = input_dir.split('/')[-1]
    newdir = input_dir.replace(
        "mnist/original_png",
        "/synth/mnist"
    )

    return newdir.replace(filename, "%s_%s"%(count,filename))

def process_mnist_img(img):
    '''Inverse, draw bounding box, resize'''

    #inverse
    inverted_image = ImageOps.invert(img)

    # draw bounding box
    draw_image = ImageDraw.Draw(inverted_image)
    width,height = inverted_image.size
    draw_image.rectangle([0,0,width-1,height-1], outline=0)

    # resize to 50% and 10 times of the original size

    new_size = random.randint(int(0.5*img.size[0]), 10*img.size[0])
    output = inverted_image.resize((new_size, new_size), Image.ANTIALIAS)

    return output

def create_synthetic_img(image_fg, image_bg):
    x_coord = random.randint(1, image_bg.size[0]-image_fg.size[0]-1)
    y_coord = random.randint(1, image_bg.size[1]-image_fg.size[1]-1)
    image_bg.paste(image_fg, (x_coord, y_coord))
    return image_bg

def main():
    ## load background files
    mnist_files = glob.glob('./mnist/original_png/*/*/*.png')
    background_files = glob.glob('./background/*.jpg')

    for i in xrange(len(mnist_files)):
        fg = Image.open(mnist_files[i])
        for j in xrange(3):
            bg = Image.open(background_files[random.randint(0,len(background_files)-1)])
            new = create_synthetic_img(process_mnist_img(fg),bg)

            # Assuming the dir is alr created, didint write the code to
            # create dir iteratively
            # dir format is the same as ""./mnist/original_png"
            new.save(get_output_dir(mnist_files[i],j))

        if not (i%500):
            print ("%s/%s"%(i, len(mnist_files)))



if __name__ == '__main__':
    main()
    print ("Done.")
