'''
VCF
c2: Position (in the reference genome)
c4: Reference (base in reference genome)*,**
c5: Alternate (base in isolate)*
c6: Quality (SNP score)

*ignore lines in which REF/ALT column contains multiple bases
**ignore lines in which the REF base is an N

'''
import argparse, os

class SNP:
	def __init__(self, position, reference, alternate, quality):
		self.position = position
		self.reference = reference
		self.alternate = alternate
		self.quality = quality

class Isolate:
	def __init__(self, name):
		self.name = name
		self.snps = {} #POSITION:SNP

def writeTABULARheader(isolates):
	header = '#position\treference'
	for isolate in isolates:
		header += '\t' + isolate.name + ' base\t' + isolate.name + ' quality'
	header += '\n'
	return header
    
def writeTABULARposition(references, isolates, position):
	pos = str(position) + '\t' + references[position]
	for isolate in isolates:
		pos += '\t'
		try:
			pos += isolate.snps[position].alternate + '\t' + isolate.snps[position].quality
		except:
			pos += references[position] + '\t' + '-'
	pos += '\n'
	return pos
    
def writeTABULAR(references, isolates):
	tabular = writeTABULARheader(isolates)
    
	positions = sorted(list(int(pos) for pos in references))
	for position in positions:
		tabular += writeTABULARposition(references, isolates, position)
    
	return tabular

def writeXCLUDE(all, xclude):
	all = open(all)
	xclude = open(xclude, 'w')
	
	for line in all:
		if line[0] == '#':
			xclude.write(line)
			continue
		if len(set(line.split('\t')[2::2])) > 1:
			xclude.write(line)
	all.close()
	xclude.close()

def splitSequence(sequence, length):
	words = []
	for i in range(0, len(sequence), length):
		words.append(sequence[i:i+length])
	return '\n'.join(words)

def writeFASTA(tabular, fasta):
	fasta = open(fasta, 'w')
	tabular = open(tabular)
    
	lines = tabular.readlines()
	
	column = 1
	fasta.write('>reference\n')
	fasta.write(splitSequence(''.join(list(line.split('\t')[1] for line in lines[1:])), 70))
	fasta.write('\n')
	
	isolates = list(' '.join(iso_base.split(' ')[:-1]) for iso_base in lines[0].split('\t')[2::2])
	column = 2
	for isolate in isolates:
		fasta.write('>' + isolate + '\n')
		fasta.write(splitSequence(''.join(list(line.split('\t')[column] for line in lines[1:])), 70))
		fasta.write('\n')
		column += 2
    
	tabular.close()
	fasta.close()
	return        

def main():
	parser = argparse.ArgumentParser(description='VCF to FASTA.')
	parser.add_argument('vcf_dir',
						metavar='vcf_dir',
						type=str,
						help='Absolute path to directory containing VCF files eg. "/home/user/vcf_dir/"')
	parser.add_argument('out_fname', 
                        metavar='out_fname',
                        type=str,
                        help='Filename for both the FASTA and tabular output (ie. supplying "snps_all" will produce the files snps_all.fasta and snps_all.tabular).')
	parser.add_argument('-x', 
                        action='store_true',
                        dest='xclude',
                        help='Also generate files that exclude SNPs common to all isolates. These will have "_x" appended to the filename provided.')
	args = parser.parse_args()
    
	references = {} #POSITION:REFERENCE
	isolates = []
	for file in os.listdir(args.vcf_dir):
		if not os.path.splitext(file)[-1] == '.vcf':
			continue
		name = os.path.splitext(file)[0]
		#print name
		isolates.append(Isolate(name))
		file_in = open(args.vcf_dir + file)
		for line in file_in:
			if line[0] == '#':
				continue
			columns = line.split('\t')
			pos = columns[1]
			#print pos
			ref = columns[3]
			#print ref
			alt = columns[4]
			if len(alt) > 1:
				print("Multiple alternate base in position ", pos, " change" , alt, " to ", alt[0])
				alt = alt[0]
			#print alt
			qual = columns[5]
			#print qual    
			if len(ref) > 1 or len(alt) > 1 or ref == 'N':
				continue #ignore see *,** above  
			references[int(pos)] = ref
			isolates[-1].snps[int(pos)] = SNP(pos, ref, alt, qual)
	tabular = open(args.vcf_dir + args.out_fname + '.tabular', 'w')
	tabular.write(writeTABULAR(references, isolates))
	tabular.close()
	
	writeFASTA(args.vcf_dir + args.out_fname + '.tabular', args.vcf_dir + args.out_fname + '.fasta')
	
	if args.xclude:
		writeXCLUDE(args.vcf_dir + args.out_fname + '.tabular', args.vcf_dir + args.out_fname + '_x.tabular')
		
		writeFASTA(args.vcf_dir + args.out_fname + '_x.tabular', args.vcf_dir + args.out_fname + '_x.fasta')
	
	
			
if __name__ == '__main__':

    main()