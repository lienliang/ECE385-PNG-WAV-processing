from PIL import Image
from bitarray import bitarray

def receiver(mode, array):
    if (mode == 'r'):
        temp = array[0:5];
    elif (mode == 'g'):
        temp = array[5:10];
    elif (mode == 'b'):
        temp = array[10:15];
    else:
        temp = array[15];
        return temp;

    transform = bitarray(3);
    transform.setall(False);
    transform.extend(temp)

    rx = transform.tobytes();
    result = int.from_bytes(rx,byteorder='little');

    return result;

path = input("Please specified the name of the file \n")

path0 = path + ".png";
img = Image.open(path0, "r")
img.show()

ramFile = open(path + ".ram", "wb")

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
        else: curPixelBytes.append(True)
        # write to file
        ramFile.write(curPixelBytes.tobytes());

ramFile.close();


#start reconstruction

test = Image.new(mode="RGB",size = (img.width, img.height));
pixels = test.load();

rgbFile = open(path + ".ram","rb");
#data = rgbFile.read();


for j in range(0,test.height,1):
    for i in range(0,test.width,1):
        idx = j * test.width + i;

        rgbFile.seek(idx*2)

        now = bitarray();
        now.fromfile(rgbFile, 2)

        red = receiver('r',now) * 8 + 3;

        green = receiver('g',now) * 8 + 3;

        blue = receiver('b',now) * 8 + 3;

        alpha = receiver('x', now);

        if (alpha):
            pixels[i,j] = (red,green,blue);
        else:
            pixels[i,j] = (0,0,0);

rgbFile.close();

test.show()

