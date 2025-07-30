# localfinder

A tool calculating weighted local correlation and enrichment significance of two tracks and finding significantly different genomic regions

## Installation Requirements

Before installing and using `localfinder`, please ensure that the following external tools are installed on your system:

- **bedtools**: Used for genomic interval operations.
  - Installation: [https://bedtools.readthedocs.io/en/latest/content/installation.html](https://bedtools.readthedocs.io/en/latest/content/installation.html)
  - conda install -c conda-forge -c bioconda bedtools 
  - mamba install -c conda-forge -c bioconda bedtools
- **ucsc-bigwigtobedgraph**: Used for converting BigWig files to BedGraph format.
  - Download: [http://hgdownload.soe.ucsc.edu/admin/exe/](http://hgdownload.soe.ucsc.edu/admin/exe/)
  - conda install -c conda-forge -c bioconda ucsc-bigwigtobedgraph
  - mamba install -c conda-forge -c bioconda ucsc-bigwigtobedgraph
- **samtools**: Used for processing SAM/BAM files.
  - Installation: [http://www.htslib.org/download/](http://www.htslib.org/download/)
  - conda install -c conda-forge -c bioconda samtools
  - mamba install -c conda-forge -c bioconda samtools

These tools are required for processing genomic data and must be installed separately.

## Installation

Install `localfinder` using `pip`:

```bash
pip install localfinder
```

## Usage

Go to github: [localfinder](https://github.com/astudentfromsustech/localfinder) for more details about usage