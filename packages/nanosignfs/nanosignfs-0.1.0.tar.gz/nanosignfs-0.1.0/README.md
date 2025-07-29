# nanosignfs

nanosignfs is a Linux-based virtual filesystem built on FUSE (Filesystem in Userspace) that seamlessly integrates cryptographic file signing into everyday write operations. Each time a file is written or modified within the mounted filesystem, it is automatically signed using a pre-configured GPG key, producing a detached .sig signature file. This mechanism ensures end-to-end integrity and non-repudiation, allowing downstream systems or auditors to verify that the content has not been tampered with. The system is particularly suited for nano-data pipelines—such as those found in scientific research, IoT, or regulated environments where even small files require cryptographic assurance. By decoupling signature logic from application logic and embedding it directly into the filesystem layer, nanosignfs simplifies compliance workflows and enhances trust in data provenance without burdening the end user.

---

##  Key Features

- Transparent FUSE mount backed by local storage
- Automatic file signing using a GPG key on each write
- Detached `.sig` signature files created per file
- Verifiable audit trail with GPG-based cryptographic integrity
- Lightweight and secure – ideal for nano-data, research pipelines, and compliance workflows

---

##  Installation

### Prerequisites

- Before using nanosignfs, make sure your system meets the following requirements:
- Operating System: Linux (with FUSE support)
- Python: 3.7+

### System Packages:

- fuse – FUSE userspace filesystem library
- gpg – GnuPG for digital signing

## Install system dependencies

- sudo yum update
- sudo yum install fuse gpg
- sudo modprobe fuse

## Author
Raghava Chellu
raghava.chellu@gmail.com

## Clone the repository

git clone https://github.com/RaghavaCh440/nanosignfs.git
cd nanosignfs


## License
MIT License

Copyright (c) 2025 Raghava Chellu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                             

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

