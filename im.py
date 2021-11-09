from PIL import Image
import argparse
import os
import sys

def LSBStenography(input, data, output):
    data_fp = open(data, "rb") # binaryS
    raw_data = data_fp.read()
    data_file_extension = os.path.splitext(data)[1] # string
    data_file_extension = data_file_extension.encode('ascii')
    #print(type(data_file_extension))
    data_size = len(raw_data)*8 # integer
    to_store = data_file_extension + data_size.to_bytes(2, byteorder='big')

    print(to_store)
    print(bin(int.from_bytes(to_store, byteorder='big')))

    #print(output)
    #im = Image.open(input).getdata()
    #newim = Image.new(im.mode, im.size)
    #width,height = im.size



def LSBStenographySanityCheck(input, data):
    if not os.path.exists(input):
        print("input file {} not found".format(input))
        sys.exit(-1)
    if not os.path.exists(data):
        print("data file {} not found".format(data))
        sys.exit(-1)
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



