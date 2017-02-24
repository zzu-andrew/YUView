import os
import subprocess
import filecmp
import hashlib
import argparse
from os import listdir
from os.path import isfile, join

qtver='5.8'
usehashforfiles = ['YUView.exe']

def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

def get_git_revision():
    return subprocess.check_output(['git', 'describe'])

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
 
def md5andversionallfiles(mypath,outfile):
    versionfile = open(outfile,'w')
    versionfile.write('Last Commit: ' + str(get_git_revision().decode('utf-8')))
    versionfile.write('Last Commit Hash: ' + str(get_git_revision_hash().decode('utf-8')))
    versionfile.write('Last Commit Hash Short: ' + str(get_git_revision_short_hash().decode('utf-8')))

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in onlyfiles:
        md5hash = md5(join(mypath,f))
        if f in usehashforfiles:
            version = str(get_git_revision_hash().decode('utf-8'))
        else:
            version = qtver
        out = f + ", " + version.rstrip() + ", " + md5hash + "\n"
        versionfile.write(out)
    versionfile.close()
            

def main():
    parser = argparse.ArgumentParser(description="Computes md5 sums for all files and also adds some git information.")
    parser.add_argument('-d', '--directory', help='Specifies the input directory.', type=str, required=True)
    parser.add_argument('-o', '--output', help='Specified the output file.', type=str, required=True)
    args = parser.parse_args()
    if args.directory is not None and args.output is not None:
        md5andversionallfiles(args.directory,args.output)
    else:
        print('An error occured. Did you specify the path and the output file?')
            

if __name__ == "__main__":
    main()