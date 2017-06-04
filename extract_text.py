#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
import os
import docx2txt
from subprocess import Popen, PIPE


def getDocxText(filename):
    try:
        text = docx2txt.process(filename)
        text = text.encode('utf-8')
        filename = filename[7:-4] + "txt"
        f = open('./TXT/'+filename,"a")
        f.write(text)
        f.close()
    except:
        print("Could not write",filename)
        pass

def getDocText(filename):
    try:
        cmd = ['antiword', filename]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        text = stdout.decode('ascii', 'ignore').encode('utf-8')
        filename = filename[7:-3] + "txt"
        f = open('./TXT/'+filename,"a")
        f.write(text)
        f.close()
    except:
        print("Could not write",filename)
        pass

for filename in os.listdir('./Docs'):
    if filename.endswith(".docx"):
        getDocxText('./Docs/'+filename)
    elif filename.endswith(".doc"):
        getDocText('./Docs/'+filename)


