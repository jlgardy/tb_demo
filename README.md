# tb_demo
*Files and instructions for an in-class demo of TB genomic epidemiology*

**1. This demo requires that you have certain software tools installed on your computer. Before attempting the tutorial, ensure that these tools are installed and functioning. If you are running a different version, the syntax may be slightly different from what is shown here.**
* BWA 0.7.13 (http://bio-bwa.sourceforge.net/index.shtml)
* samtools 1.3 (http://www.htslib.org)
* bcftools 1.3 (http://www.htslib.org)
* Mykrobe TB (not Mykrobe MRSA!) (http://www.mykrobe.com/products/predictor/#tb)
    
    
**2. You will also need to download the data files we'll be using, which are provided to you via this repo. You'll need:**
- the *M. tuberculosis* H37Rv reference genome: [reference.fa](reference.ga) - this is version NC000962.3 of the genome 
- the paired-end sequencing data from our three patients's TB isolates (note that these are abbreviated versions of the full files, shortened to improve the speed of the demo): 
  - [patient_1_1.fastq.gz](patient_1_1.fastq.gz) & [patient_1_2.fastq.gz](patient_1_2.fastq.gz)
  - [patient_2_1.fastq.gz](patient_2_1.fastq.gz) & [patient_2_2.fastq.gz](patient_2_2.fastq.gz)
  - [patient_3_1.fastq.gz](patient_3_1.fastq.gz) & [patient_3_2.fastq.gz](patient_3_2.fastq.gz)


**3. Make a directory called tb_demo and place your downloaded reference genome and sequencing data there:**

`mkdir tb_demo` creates the directory

`mv reference.fa tb_demo` moves the reference genome to the tb_demo directory (this command will vary depending on where you downloaded your data to and where you created the tb_demo directory)

`mv *.fastq.gz tb_demo` moves the data to the tb_demo directory (as above, this may vary depending on where you created things)

`gunzip *.gz` unzips the compressed fastq files


**4. Index the reference genome. This only needs to be done once, anytime you download a new reference genome:**

`bwa index reference.fa` 


**5. Map the paired-end reads from each patient's isolate against the reference using bwa mem:**

`bwa mem reference.fa reads1.fastq reads2.fastq > outfiile.sam` is the general syntax you'd use

`bwa mem reference.fa patient1_1.fastq patient1_2.fastq > patient_1.sam` is an example using the data from patient_1's isolate


**6. For each SAM file, we must do a few operations to make it efficient to work with. We will use three different samtools utilities - view, sort, and index:**

`samtools view -b file.sam > file.bam` is the general syntax you'd use to **convert** the text SAM file to the binary BAM format

`samtools view -b patient_1.sam > patient_1.bam` is an example using the data from patient_1's isolate

`samtools sort file.bam -o file.sorted` is the general syntax you'd use to **sort** the BAM 

`samtools sort patient_1.bam -o patient_1.sorted` is an example using the data from patient_1's isolate

`samtools index file.sorted` is the general syntax you'd use to **index** the BAM 

`samtools index patient_1.sorted` is an example using the data from patient_1's isolate


**7. For each sorted, indexed BAM file, we will generate a pileup file summarizing the mapping at each position relative to our reference genome:**

`samtools mpileup -q 30 -u -f reference.fa file.sorted > file.bcf -I` is the general syntax you'd use

`samtools mpileup -q 30 -u -f reference.fa patient_1.sorted > patient_1.bcf -I` is an example using the data from patient_1's isolate


**8. For each pileup file, we will convert it to a human-readable format and, at the same time, extract only those positions at which our genome is different from the reference genome - the variants:**

`bcftools call -O v -mv file.bcf > file.vcf` is the general syntax you'd use

`bcftools call -O v -mv patient_1.bcf > patient_1.vcf` is an example using the data from patient_1's isolate
