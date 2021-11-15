from PIL import Image
import bitarray
import argparse
import os
import sys

def setBit(num, value):
    num = list(bin(num))
    num[-1] = str(value)
    num = ''.join(num)
    return int(num,2)

def pad_bitarray(myArray):
    addition = 32 - len(myArray)
    to_add = ''
    for i in range(addition):
        to_add += '0'
    a = bitarray.bitarray(to_add)
    #(to_add)
    a.extend(myArray)
    return a

def LSBStenography(input, data, output):
    data_fp = open(data, "rb")
    raw_data = data_fp.read() # read as bytes object
    data_ba = bitarray.bitarray()
    data_ba.frombytes(raw_data)
    data_ba.fill()

    extension_ba = bitarray.bitarray()
    extension_ba.frombytes(os.path.splitext(data)[1].encode('ascii'))
    extension_ba = pad_bitarray(extension_ba)

    length_ba = bitarray.bitarray(bin(len(raw_data)*8)[2:])
    length_ba = pad_bitarray(length_ba)

    store_ba = extension_ba + length_ba + data_ba

    img = Image.open(input)

    x = 0
    rgb = 0
    t = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = list(img.getpixel((i,j)))

            if(x <= len(store_ba)-3):
                pixel[0] = setBit(pixel[0], store_ba[x])
                pixel[1] = setBit(pixel[1], store_ba[x+1])
                pixel[2] = setBit(pixel[2], store_ba[x+2])
                x+=3
            elif (x <= len(store_ba)-2):
                pixel[0] = setBit(pixel[0], store_ba[x])
                pixel[1] = setBit(pixel[1], store_ba[x+1])
                x+=2
            elif (x <= len(store_ba)-1):
                pixel[0] = setBit(pixel[0], store_ba[x])
                x+=1
            img.putpixel((i,j), tuple(pixel))

    img.save(output)
    print("Wrote {} bytes of data to {}".format(len(store_ba), output))



def LSBStenographySanityCheck(input, data):
    if not os.path.exists(input): # check the image file exists
        print("Input file {} not found".format(input))
        sys.exit(-1)
    
    if os.path.splitext(input)[1].lower() != '.png' and os.path.splitext(input)[1].lower() != '.jpg':
        print("Input file not .png. Invalid format")
        sys.exit(-1)

    if not os.path.exists(data): # check the data file exists
        print("Data file {} not found".format(data))
        sys.exit(-1)
    # Checks data can fit in the space provided in the image   
    with Image.open(input) as image:
        hidingSpace = len(image.getdata())*3
    with open(data, 'rb') as data:
        toHide = len(data.read()*8)
    if hidingSpace < toHide:
        print("Data is too large to hide.\nHiding space for the given image: {}, Data size: {}".format(hidingSpace, toHide))
        return 1

    return 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Simple LSB Stenography')
    ap.add_argument('input', metavar='input', help='file to hide information in')
    ap.add_argument('data', metavar='data', help='data to hide within the input')
    ap.add_argument('--output', metavar='output', help='output file name')
    args = ap.parse_args()

    if LSBStenographySanityCheck(args.input, args.data):
        sys.exit(-1)

    if args.output is None:
        LSBStenography(args.input, args.data, os.path.splitext(args.input)[0]+'_modified'+os.path.splitext(args.input)[1])
    else:
        LSBStenography(args.input, args.data, args.output)



