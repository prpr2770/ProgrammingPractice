
import os
import sys


if __name__=="__main__":
    dir = "/Users/uchiha/Downloads/Fall2022Courses/Sriram_AdvDataStructures/hw1/"
    dfiles = [ 'war_and_peace_tolstoy.txt', 'hemingway-sun-also-rises.txt', 'anna_karenina_tolstoy.txt', 'bacterial_genome_2.txt', 'hemingway-stories-poems.txt', 'bacterial_genome_1.txt', 'monkeypox-genome.txt', 'hemingway-in-our-time.txt']
    print(dfiles)
    segs = []
    for fname in dfiles:
        fn = dir + fname
        with open(fn) as f: 
            seg = f.read(20)
            if not seg:
                print("Error reading: %s" % fn) 
            segs.append(seg)
    
    for fn,seg in zip(dfiles, segs): 
        print("%s\t\t%s\n" %(fn,seg) )

