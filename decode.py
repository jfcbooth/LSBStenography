from PIL import Image
import bitarray
from bitarray import util
import argparse
import os
import sys

def LSBStenographyDecrypt(input):

    img = Image.open(input)
    read = []
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # read file extension and size of data
            pixel = list(img.getpixel((i,j)))
            read.append(pixel[0] & 1)
            read.append(pixel[1] & 1)
            read.append(pixel[2] & 1)
    

    extension_ba = bitarray.bitarray(read[0:32])
    extension_bytes = extension_ba.tobytes()
    extension = extension_bytes.decode('ascii')
    print("Found data type: {}".format(extension))

    length = util.ba2int(bitarray.bitarray(read[32:64]))

    data_ba = bitarray.bitarray(read[64:length+64])
    data_bytes = data_ba.tobytes()
    data = data_bytes.decode('ascii')
    print("Found {} bytes of data.".format(len(data)))


    with open(os.path.splitext(input)[0] + '_data' + extension, 'wb') as fp:
        data_ba.tofile(fp)
    print("Data written to {}".format(os.path.splitext(input)[0] + '_data' + extension))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Simple LSB Stenography')
    ap.add_argument('input', metavar='input', help='file to find information in')
    args = ap.parse_args()

    LSBStenographyDecrypt(args.input)

