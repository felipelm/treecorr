import os
from datetime import datetime

class Treecorr():
    def __init__(self, process, files, config, input, output, SIM):
        self.process = process
        self.files = files
        self.output = output
        self.input = input
        self.SIM = SIM
        self.config = config
        self.init_templates()
        self.process_datetime = process + "_" + datetime.now().strftime("%Y-%M-%d_%H%M%S")
        self.output_path = os.path.join(output, self.process_datetime)
        self.condor_files = []

    def init_templates(self):
        self.condor_str = str()
        condor_file = '{}/submit.condor'.format(self.config)
        with open(condor_file, 'r') as infile:
            for line in infile:
                self.condor_str = self.condor_str+line

        self.run_str = str()
        run_file = '{}/run.sh'.format(self.config)
        with open(run_file, 'r') as infile:
            for line in infile:
                self.run_str = self.run_str+line

    def open_or_create_file(filename, text):
        try:
            os.makedirs(os.path.dirname(filename))
        except:
            ''

        with open(filename, 'w') as outfile:
            outfile.write(text)

    def create_condor_args(self, exec_file, f1, f2=''):
        logname = os.path.join(self.output, 'log{}{}'.format(f1, f2))
        return self.condor_str.format(logname=logname, arguments=exec_file)
    
    def create_run_args(self, f1, f2=''):
        configuration = "{config}/{process}.yaml".format(config=self.config, process=self.process)
        output_filename = "{process}_file_name={output}/xi_{process}_{file1}{file2}_{SIM}.fits".format(
            process=self.process, output=self.output, file1=f1, file2=f2, SIM=self.SIM)
        file_name = "{input}/{file1}.fits".format(file1=f1, input=self.input)
        file_name2 = "{input}/{file2}.fits".format(file2=f2, input=self.input)
        if f2 == '':
            arguments = "{} {} {}".format(configuration, file_name, output_filename)
        else:
            arguments = "{} {} {} {}".format(configuration, file_name, file_name2, output_filename)
        return arguments

    def create_run_files(self, f1, f2=''):
        arguments = self.create_run_args(f1, f2)
        run_text = self.run_str.format(arguments=arguments)

        run_filename = "run{}_{}{}.sh".format(self.process, f1, f2)
        filename = os.path.join(self.output_path, run_filename)
        self.open_or_create_file(filename, run_text)
    
    def create_condor_files(self, f1, f2=''):
        condor_filename = "{}_z{}z{}.condor".format(self.process, f1, f2)
        filename = os.path.join(self.output_path, condor_filename)
        self.condor_files.append(filename)
        condor_text = self.create_condor_args(f1, f2)

        self.open_or_create_file(filename, condor_text)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--process", help="Simulation process name. Possible values: nn, ng or gg", required=True)
    parser.add_argument(
        "--files", help="File Combinations. Default: 1,2,3,4,5", type=str, default='1,2,3,4,5')
    parser.add_argument("--output", help="Output directory",
                        type=str, required=True)
    parser.add_argument("--input", help="Input directory", type=str, required=True)
    parser.add_argument("--config", help="config directory", type=str, required=True)
    parser.add_argument("--SIM", help="Simulation", type=str, default='default')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print('Input diretory invalid')
        exit(1)

    if not os.path.exists(args.config):
        print('Configuration diretory invalid')
        exit(1)

    if not os.path.exists(args.output):
        print('Output diretory invalid')
        exit(1)

    tc = Treecorr(args.process, args.files, args.config, args.input, args.output, args.SIM)

