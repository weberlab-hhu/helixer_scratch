import os
import random
random.seed(9)
allsp = os.listdir('../refseq')
allsp = [x for x in allsp if x.find('.sh') < 0]

# In AUGUSTUS is a list of the refseq species
# for which there are augustus models available
# this was made by hand, as names don't necessarily
# perfectly match... both in terms of simple things
# like capitalization, but also other things like
# writhing 'sp.' or somthing having been taxonomically
# re-named. There are likely errors/missed models.
with open('in_augustus.txt') as f:
    augsp = f.readlines()
augsp = [x.rstrip() for x in augsp]
notaugsp = [x for x in allsp if x not in augsp]

# 
random.shuffle(augsp)
random.shuffle(notaugsp)

train_max_frac = 0.7
last_aug_train = int(len(augsp) * train_max_frac)
last_notaug_train = int(len(notaugsp) * train_max_frac)

with open('set_assignments.csv', 'w') as f:
    # split augustus models separate from the rest, to guarantee
    # a good chunk of them lands in both test and train, respectively 
    for i, sp in enumerate(augsp):
        dlset = "train" if i <= last_aug_train else "test"
        f.write(f'{sp},{dlset}\n')
    for i, sp in enumerate(notaugsp):
        dlset = "train" if i <= last_notaug_train else "test"
        f.write(f'{sp},{dlset}\n')
