===
FAQ
===

How should I cite pysam
=======================

Pysam has not been published in print. When referring to pysam, please
use the github URL: https://github.com/pysam-developers/pysam. 
As pysam is a wrapper around htslib and the samtools package, I
suggest citing [Li.2009]_, [Bonfield.2021]_, and/or [Danecek.2021]_,
as appropriate.

Is pysam thread-safe?
=====================

Pysam is a mix of python and C code. Instructions within python are
generally made thread-safe through python's `global interpreter lock`_
(:dfn:`GIL`). This ensures that python data structures will always be in a
consistent state. 

If an external function outside python is called, the programmer has a
choice to keep the GIL in place or to release it. Keeping the GIL in
place will make sure that all python threads wait until the external
function has completed. This is a safe option and ensures
thread-safety.

Alternatively, the GIL can be released while the external function is
called. This will allow other threads to run concurrently. This can be
beneficial if the external function is expected to halt, for example
when waiting for data to read or write. However, to achieve
thread-safety, the external function needs to be implemented with
thread-safety in mind. This means that there can be no shared state
between threads, or if there is shared, it needs to be controlled to
prevent any access conflicts.

Pysam generally uses the latter option and aims to release the GIL for
I/O intensive tasks. This is generally fine, but thread-safety of all
parts have not been fully tested. 

A related issue is when different threads read from the same file
object - or the same thread uses two iterators over a file. There is
only a single file-position for each opened file. To prevent this from
happening, use the option ``multiple_iterators=True`` when calling
a fetch() method. This will return an iterator on a newly opened
file.

pysam coordinates are wrong
===========================

pysam uses 0-based coordinates and the half-open notation for ranges
as does python. Coordinates and intervals reported from pysam always
follow that convention.

Confusion might arise as different file formats might have different
conventions. For example, the SAM format is 1-based while the BAM
format is 0-based. It is important to remember that pysam will always
conform to the python convention and translate to/from the file format
automatically.

The only exception is the :term:`region` string in the
:meth:`~pysam.AlignmentFile.fetch` and
:meth:`~pysam.AlignmentFile.pileup` methods. This string follows the
convention of the samtools command line utilities. The same is true
for any coordinates passed to the samtools command utilities directly,
such as :meth:`pysam.mpileup`.

Calling pysam.fetch() confuses existing iterators
=================================================

The following code will cause unexpected behaviour::

   samfile = pysam.AlignmentFile("pysam_ex1.bam", "rb")

   iter1 = samfile.fetch("chr1")
   print(next(iter1).reference_id)
   iter2 = samfile.fetch("chr2")
   print(next(iter2).reference_id)
   print(next(iter1).reference_id)

This will give the following output::

    0
    1
    Traceback (most recent call last):
      File "xx.py", line 8, in <module>
        print(next(iter1).reference_id)
      File "libcalignmentfile.pyx", line 2103,
      in pysam.libcalignmentfile.IteratorRowRegion.__next__
    StopIteration

Note how the second iterator stops as the file pointer has moved to
chr2. The correct way to work with multiple iterators is::

   samfile = pysam.AlignmentFile("pysam_ex1.bam", "rb")

   iter1 = samfile.fetch("chr1", multiple_iterators=True)
   print(next(iter1).reference_id)
   iter2 = samfile.fetch("chr2")
   print(next(iter2).reference_id)
   print(next(iter1).reference_id)

Here, the output is::

   0
   1
   0

The reason for this behaviour is that every iterator needs to keep
track of its current position in the file. Within pysam, each opened
file can only keep track of one file position and hence there can only
be one iterator per file. Using the option ``multiple_iterators=True``
will return an iterator within a newly opened file. This iterator will
not interfere with existing iterators as it has its own file handle
associated with it.

Note that re-opening files incurs a performance penalty which can
become severe when calling :meth:`~pysam.AlignmentFile.fetch` often.
Thus, ``multiple_iterators`` is set to ``False`` by default.

AlignmentFile.fetch does not show unmapped reads
================================================

By default, :meth:`~pysam.AlignmentFile.fetch` will only iterate over
placed alignments in the SAM/BAM/CRAM file. Thus the following always
works::

    f = pysam.AlignmentFile(fname, "r")
    for r in f.fetch():
        assert r.reference_name is not None

If the file contains unaligned reads, they can be included
in the iteration by adding the ``until_eof=True`` flag::

    f = pysam.AlignmentFile(fname, "r")
    for r in f.fetch(until_eof=True):
        if r.is_unmapped:
            print("read is unmapped")

See also :meth:`fetch("*") <pysam.AlignmentFile.fetch>` which iterates
only over the unplaced unmapped reads at the end of the file.

I can't call AlignmentFile.fetch on a file without an index
===========================================================

:meth:`~pysam.AlignmentFile.fetch` requires an index when
iterating over a SAM/BAM file. To iterate over a file without an
index, use ``until_eof=True``::

    bf = pysam.AlignmentFile(fname, "rb")
    for r in bf.fetch(until_eof=True):
        print(r)

	
BAM files with a large number of reference sequences are slow
=============================================================

If you have many reference sequences in a BAM file, the following
might be slow::

      track = pysam.AlignmentFile(fname, "rb")
      for aln in track.fetch():
      	  pass
	  
The reason is that track.fetch() will iterate through the BAM file
for each reference sequence in the order as it is defined in the
header. This might require a lot of jumping around in the file. To
avoid this, use::

      track = pysam.AlignmentFile(fname, "rb")
      for aln in track.fetch(until_eof=True):
      	  pass
 
This will iterate through reads as they appear in the file.

Weirdness with spliced reads in samfile.pileup(chr,start,end) given spliced alignments from an RNA-seq bam file
===============================================================================================================

Spliced reads are reported within samfile.pileup. To ignore these
in your analysis, test the flags ``is_del == True and indel == 0``
in the :class:`~.PileupRead` object.

I can't edit quality scores in place
====================================

Editing reads in-place generally works, though there is one
quirk to be aware of. Assigning to AlignedSegment.query_sequence will invalidate 
any quality scores in AlignedSegment.query_qualities. The reason is that samtools
manages the memory of the sequence and quality scores together 
and thus requires them to always be of the same length or 0.

Thus, to in-place edit the sequence and quality scores, copies of
the quality scores need to be taken. Consider trimming for example::

    quals = read.query_qualities
    read.query_sequence = read.query_sequence[5:10]
    read.query_qualities = quals[5:10]
 
Why is there no SNPCaller class anymore?
=========================================

SNP calling is highly complex and heavily parameterized. There was a
danger that the pysam implementations might show different behaviour from the
samtools implementation, which would have caused a lot of confusion.

The best way to use samtools SNP calling from python is to use the 
:meth:`pysam.mpileup` command and parse the output directly.

I get an error 'PileupProxy accessed after iterator finished'
=============================================================

Pysam works by providing proxy objects to objects defined within
the C-samtools package. Thus, some attention must be paid to the
lifetime of objects. The following to code snippets will cause an
error::

    s = AlignmentFile('ex1.bam')
    for p in s.pileup('chr1', 1000,1010):
        pass
    
    for pp in p.pileups:
        print(pp)

The iteration has finished, thus the contents of ``p`` are invalid. Another
variation of this::

    p = next(AlignmentFile('ex1.bam').pileup('chr1', 1000, 1010))
    for pp in p.pileups:
        print(pp)

Again, the iteration finishes as the temporary iterator created
by pileup goes out of scope. The solution is to keep a handle
to the iterator that remains alive::

    i = AlignmentFile('ex1.bam').pileup('chr1', 1000, 1010)
    p = next(i)
    for pp in p.pileups:
        print(pp)

Pysam won't compile
===================

Compiling pysam can be tricky as there are numerous variables that
differ between build environments such as OS, version, python version,
and compiler. It is difficult to build software that builds cleanly
on all systems and the process might fail. Please see the 
`pysam user group
<https://groups.google.com/forum/#!forum/pysam-user-group>`_
for common issues.

If there is a build issue, read the generated output carefully -
generally the cause of the problem is among the first errors to be
reported. For example, you will need to have the development version
of python installed that includes the header files such as
:file:`Python.h`. If that file is missing, the compiler will report
this at the very top of its error messages but will follow it 
with any unknown function or variable definition it encounters later
on.

General advice is to always use the latest version on python_ and
cython_ when building pysam. There are some known incompatibilities:

* Python 3.4 requires cython 0.20.2 or later (see `here
  <https://github.com/pysam-developers/pysam/issues/37>`_)

.. _global interpreter lock: https://en.wikipedia.org/wiki/Global_interpreter_lock

ImportError: cannot import name csamtools
=========================================

In version 0.10.0 and onwards, all pysam extension modules contain a
``lib``-prefix. This facilates linking against pysam extension modules
with compilers that require to start with ``lib``. As a consequence,
all code using pysam extension modules directly will need to be
adapted. For example,::

   cimport pysam.csamtools

will become::

   cimport pysam.libcsamtools

