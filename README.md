# LSBStenography

Basic python exercise using least signficiant bit stengography to hide information in images. It can hide any type of information (pictures, text, binary, etc.) into a PNG. It might work with other image formats, but it hasn't been tested.

# Usage
To hide a file in an image:
`python encrypt.py <input_image> <data_to_hide> --output <output_image>`

To discover the data that has been hidden in an image:
`python decrypt.py <image>`