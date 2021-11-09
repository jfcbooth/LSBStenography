from PIL import Image
import bitarray
import argparse
import os
import sys

def pad_data(data_str, size):
    addition = 32 - len(data_str)
    to_add = ''
    for i in range(addition):
        to_add +='0'
    return to_add + data_str


def LSBStenography(input, data, output):
    data_fp = open(data, "rb")
    raw_data = data_fp.read() # read as bytes object

    ba = bitarray.bitarray()
    ba.frombytes(os.path.splitext(data)[1].encode('ascii'))
    ba.fill()

    ba2=bitarray.bitarray(len(raw_data)*8)
    ba2.fill()

    print(len(ba2))
    print(ba2)
    #os.path.splitext(data)[1].encode('ascii'))
    #data_file_extension = os.path.splitext(data)[1].encode('ascii') # read file extension in binary
    #binary_data_file_extension = bin(int.from_bytes(data_file_extension, byteorder='big'))[2:]
    # pad data to a length of 32
    #binary_data_file_extension = pad_data(binary_data_file_extension, 32)
    #binary_data_size = pad_data(bin(len(raw_data)*8)[2:], 32)

    #print(type(binary_data_file_extension))
    #print(type(binary_data_size))
    #print(type(raw_data))
    #to_store = binary_data_file_extension + binary_data_size + raw_data
    #print(to_store)

    #final = bin(int.from_bytes(binary_data_file_extension + binary_data_size + raw_data, byteorder='little'))
    #print(len(final))

    #print(output)
    #im = Image.open(input).getdata()
    #newim = Image.new(im.mode, im.size)
    #width,height = im.size



def LSBStenographySanityCheck(input, data):
    if not os.path.exists(input): # check the image file exists
        print("Input file {} not found".format(input))
        sys.exit(-1)
    
    if os.path.splitext(input)[1] != '.png':
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



