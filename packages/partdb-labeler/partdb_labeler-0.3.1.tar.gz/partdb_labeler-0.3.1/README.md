partdb-labeler
==============

![example](./doc/example.jpg)

Connects to a [PartDB](https://github.com/Part-DB/Part-DB-server) server, grabs info for a selected part, and formats a label to
be printed on an EPL2-compatible label printer.  Command-line options enable configuration of the label size, server to use, 
and more.

Why did I write this?
---------------------

PartDB has a label generator built-in, but it only produces PDFs that must then be rasterized and printed.  This works well 
enough if you're sending labels to a laser printer, but I found that QR codes small enough to fit on the label stock I wanted
to use weren't scannable.  This generator speaks EPL2, one of the languages used by Zebra label printers, to produce 
precisely-formatted labels with QR codes that scan easily with your phone or a dedicated barcode scanner.

Compatibility
-------------

So far, it's been tested with two Zebra printers: an LP2844 and a GK420t.  The LP2844 was driven by an Arch Linux system with
a CUPS print queue feeding it through a network print server.  The GK420t was driven by a Windows 11 system, connected to the
printer via USB.  

Usage
-----

```partdb_labeler -h``` will show you the available options.

For convenience, you might also consider adding a short shell script somewhere in your PATH that will call the Python module
with your server configuration.  I use this (the API key is a read-only key I've publicized elsewhere):

```
#!/usr/bin/env bash
partdb_labeler -p https://partdb.alfter.us -k tcp_673fc81f0b7837ca4c029fbd6536b27742eb8b742eba27bf547c8136dc6a84f8 $*
```

or the same, as a batch file on Windows:

```
@echo off
partdb_labeler -p https://partdb.alfter.us -k tcp_673fc81f0b7837ca4c029fbd6536b27742eb8b742eba27bf547c8136dc6a84f8 %*
```
