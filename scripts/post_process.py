import os,sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", 
		    help="input file containing labels in format:  fname score xmin ymin xmax ymax",
		    required=True
                  )

parser.add_argument("-o","--output", help="Output directory to write files", default='predictions')
parser.add_argument("--thresh", default=0.5, help="set iou threshold for filtering", type=float)

args = vars(parser.parse_args())

def infer_label(name):
    return name.split('.')[0].split('_')[-1]

thresh = args["thresh"]
label = infer_label(args["input"])

with open(args["input"], 'r') as f:
    lines = f.readlines()
    for line in lines:
        values = line.split()
        file_name = values[0]
        confidence = float(values[1])
        if not os.path.isdir(args["output"]):
            os.mkdir(args["output"])
        out_file = open(os.path.join(args["output"],file_name + '.txt'), 'a+')
        
        if confidence > thresh:
            out_file.write("%s %s %s %s %s %s\n" %(label, values[1], values[3], values[2], values[5], values[4]))
        out_file.close()
