# source /mnt/eups/linea_eups_setup.sh
# setup treecorr 3.3.7+0

# with open(newfile, 'w') as outfile:
#     with open(oldfile, 'r') as infile:
#         for line in infile:
#             outfile.write(line)
# python run.py --process ng
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--process", help="Simulation process name. Possible values: nn, ng or gg", required=True)
parser.add_argument("--files", help="File Combinations. Default: 1,2,3,4,5", type=str, default='1,2,3,4,5')
parser.add_argument("--output", help="Output directory", type=str, default='/Users/felipemachado/repos/pipelines')
parser.add_argument("--input", help="Input directory", type=str, default='/Users/felipemachado/repos/pipelines')
parser.add_argument("--SIM", help="Simulation", type=str, default='default')

args = parser.parse_args()

process = args.process
files = args.files  
output = args.output
input = args.input
SIM = args.SIM

if process == 'nn':
  for f1 in files.split(','):
    print("corr2 nn.yaml file_name=lens-cat_z{file1}.fits nn_file_name=xi_nn_{file1}_{SIM}.fits".format(file1=f1, SIM=SIM))
else:
  for f1 in files.split(','):
    for f2 in files.split(','):
      print("corr2 {process}.yaml file_name=lens-cat_z{file1}.fits file_name2=src-cat_z{file2}.fits {process}_file_name=xi_{process}_{file1}{file2}_{SIM}.fits".format(file1=f1, file2=f2, SIM=SIM, process=process))
 

# condor_str = str()
# condor_file = 'submit.condor'
# with open(condor_file, 'r') as infile:
#     for line in infile:
#         condor_str=condor_str+line

# x=condor_str.format(logname='/app/lala', arguments='teste 13')
# print(x)
