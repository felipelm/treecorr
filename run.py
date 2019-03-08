# python run.py --process ng
import argparse
import os
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument("--process", help="Simulation process name. Possible values: nn, ng or gg", required=True)
parser.add_argument("--files", help="File Combinations. Default: 1,2,3,4,5", type=str, default='1,2,3,4,5')
parser.add_argument("--output", help="Output directory", type=str, required=True)
parser.add_argument("--input", help="Input directory", type=str, required=True)
parser.add_argument("--SIM", help="Simulation", type=str, default='default')

args = parser.parse_args()

process = args.process
files = args.files  
output = args.output
input = args.input
SIM = args.SIM

if not os.path.exists(input):
  print('Input diretory invalid')
  exit(1)

if not os.path.exists(output):
  print('Output diretory invalid')
  exit(1)

condor_str = str()
condor_file = 'submit.condor'
with open(condor_file, 'r') as infile:
    for line in infile:
        condor_str=condor_str+line

executable = "/mnt/eups/packages/Linux64/treecorr/3.3.7+0/bin/corr2"

x = condor_str.format(logname=os.path.join(output, 'log'),
                      arguments='teste 13', executable=executable)

process_datetime = datetime.now().strftime("%Y-%M-%d_%H%M%S")
condor_files=[]
output_path = os.path.join(output, process_datetime)
if process == 'nn':
  for f1 in files.split(','):
    arguments = "nn.yaml file_name={input}/lens-cat_z{file1}.fits nn_file_name={output}/xi_nn_{file1}_{SIM}.fits".format(
        file1=f1, SIM=SIM, input=input, output=output_path)
    submit_str = condor_str.format(logname=os.path.join(output_path, 'log{}'.format(f1)),
                                   arguments=arguments, executable=executable)
    condor_filename = "{}_{}.condor".format(process, f1)
    filename = os.path.join(output_path, condor_filename)
    condor_files.append(filename)
    try:
      os.makedirs(os.path.dirname(filename))
    except:
      ''

    with open(filename, 'w') as outfile:
      outfile.write(submit_str)
else:
  for f1 in files.split(','):
    for f2 in files.split(','):
      arguments = "{process}.yaml file_name={input}/lens-cat_z{file1}.fits file_name2={input}/src-cat_z{file2}.fits {process}_file_name={output}/xi_{process}_{file1}{file2}_{SIM}.fits".format(
          file1=f1, file2=f2, SIM=SIM, process=process, input=input, output=output_path)
      submit_str = condor_str.format(logname=os.path.join(output_path, 'log{}{}'.format(f1, f2)),
                                    arguments=arguments, executable=executable)
      condor_filename = "{}_z{}z{}.condor".format(process, f1, f2)
      filename = os.path.join(output_path, condor_filename)
      condor_files.append(filename)
      try:
        os.makedirs(os.path.dirname(filename))
      except:
        ''

      with open(filename, 'w') as outfile:
        outfile.write(submit_str)
 
print(condor_files)
# os.system('ls')
os.system('source /mnt/eups/linea_eups_setup.sh')
os.system('setup treecorr 3.3.7+0')
