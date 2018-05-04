from PIL import Image
from bitarray import bitarray
import os;
import binascii;

path = input("Please specified the name of the file \n")

path0 = path + ".png";
img = Image.open(path0, "r")

txtFile = open(path + ".txt", "w")

for j in range(0,img.height,1):
    for i in range(0,img.width,1):
        pixel = img.getpixel((i,j));

        temp_r = pixel[0] // 8;
        temp_g = pixel[1] // 8;
        temp_b = pixel[2] // 8;

        #if (len(pixel) > 3):
            #alpha = pixel[3];
        if (i == (img.width - 1) and j < (img.height - 1)):
            pixel_next = img.getpixel((0,j + 1));
        elif (i == (img.width - 1) and j == (img.height - 1)):
            pixel_next = img.getpixel((0,0));
        else:
            pixel_next = img.getpixel((i + 1, j));

        if (pixel[0] == 163 and pixel[1] == 73 and pixel[2] == 164):
            alpha = 0;
        else:
            alpha = 100;

        temp_pixel = [temp_r, temp_g, temp_b ]

        curPixelBytes = bitarray();
        for i in range(0, 3, 1):
            curPBit = '{0:05b}'.format(temp_pixel[i])

            for k in range(0, 5, 1):
                if (curPBit[k] == '1'):
                    curPixelBytes.append(True);
                else:
                    curPixelBytes.append(False);

        if (alpha < 20):
            curPixelBytes.append(False)
            display = 0;
        else:
            curPixelBytes.append(True)
            display = 1;
        # write to file

        string = '{0:05b}'.format(temp_pixel[0]) + '{0:05b}'.format(temp_pixel[0]) + '{0:05b}'.format(temp_pixel[0]) + display.__str__()
        #print(string)
        temp = hex(int(string, 2))
        #print(temp[2:6])
        txtFile.write(temp[2:6])
        txtFile.write(os.linesep)


txtFile.close();

