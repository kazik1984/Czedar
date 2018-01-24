'''
Created on 21 paz 2016

@author: PI345811
'''

user='cgsysadm'
passw='cgsysadm_t13'
sid='t13bscs'
host='aixtestdb1.unx.era.pl'
port=1521
#tmcode='select utils.get_tmcode({},{}) from dual'.format()
svlcode='select svlcode from mpulktmm where tmcode={} and spcode={} and sncode={}'.format(572,107,1)


database='cgsysadm/cgsysadm_t13@t13bscs'
print(database.split('/')[0])
print(database.split('/')[1].split('@')[0])
print(database.split('/')[1].split('@')[1])
    