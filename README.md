# tb_demo
*Files and instructions for an in-class demo of TB genomic epidemiology*

**1. This demo requires that you have certain software tools installed on your computer. Before attempting the tutorial, ensure that these tools are installed and functioning. If you are running a different version, the syntax may be slightly different from what is shown here.**
* BWA 0.7.13 (http://bio-bwa.sourceforge.net/index.shtml)
* samtools 1.3 (http://www.htslib.org)
* bcftools 1.3 (http://www.htslib.org)
* bedtools (http://bedtools.readthedocs.io/en/latest/) 
* Mykrobe TB (not Mykrobe MRSA!) (http://www.mykrobe.com/products/predictor/#tb)
    
**2. You will also need to download the data files we'll be using, which are provided to you via this repo. You'll need:**
- the *M. tuberculosis* H37Rv reference genome: [reference.fa](reference.ga) - this is version NC000962.3 of the genome 
- the paired-end sequencing data from our three patients (note that these are abbreviated versions of the full files, shortened to improve the speed of the demo): 
  - [patient_1_1.fastq.gz](patient_1_1.fastq.gz) & [patient_1_2.fastq.gz](patient_1_2.fastq.gz)
  - [patient_2_1.fastq.gz](patient_2_1.fastq.gz) & [patient_2_2.fastq.gz](patient_2_2.fastq.gz)
  - [patient_3_1.fastq.gz](patient_3_1.fastq.gz) & [patient_3_2.fastq.gz](patient_3_2.fastq.gz)


**3. Make a directory called tb_demo and place your downloaded reference genome and sequencing data there:**

`mkdir tb_demo` creates the directory

`mv reference.fa tb_demo` moves the reference genome to the tb_demo directory (this command will vary depending on where you downloaded your data to and where you created the tb_demo directory)

`mv *.fastq.gz tb_demo` moves the data to the tb_demo directory (as above, this may vary depending on where you created things)

`gunzip *.gz` unzips the compressed fastq files

