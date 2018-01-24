'''
Created on 21 paz 2016

@author: PI345811
'''
preCommand='. ./.profile;'
rps=preCommand+'for p in data pteh teh rdh dih fih prih rih udh stonoga fuh rlh ecch; do ps -fu $USER|egrep -v "sshd|oracle" | grep -E "[ /]$p( .*)?$" | sort -k 9; done'

readASCIIconvGsm=preCommand+'cat $BSCS_WORK/MP/SWITCH/ASCII/GSM/asciiconv.ini'
echoBSCS_WORK=preCommand+'echo $BSCS_WORK'