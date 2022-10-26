<h1 align="center">
  <br>
    <img src="https://raw.githubusercontent.com/cybersecsi/topmostp/main/logo.png" alt= "topmostp" width="300px">
</h1>
<p align="center">
    <b>topmostp</b>
<p>

<p align="center">
  <a href="https://github.com/cybersecsi/topmostp/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>
  <a href="https://github.com/cybersecsi/topmostp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
</p>

## Table of Contents
- [Overview](#overview)
- [Install](#install)
- [Usage](#usage)
- [Demo](#demo)
- [Credits](#credits)
- [License](#license)

## Overview
``topmostp`` (**Topmost P**orts) is a tool that allows you to quickly retrieve the **most used ports**. The source of the ranking is the ``nmap-services`` in the [nmap repo](https://raw.githubusercontent.com/nmap/nmap/master/nmap-services).

At [SecSI](https://secsi.io) we found it useful to get this information to use it in a **pipeline of scripts**.

## Install
You can easily install it by running:
```
pip install topmostp
```

## Usage
```
topmostp --help
```

This will display help for the tool. Here are all the commands it supports.

```
 Usage: topmostp [OPTIONS] COMMAND [ARGS]...                                                         
                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────╮
│ find     Find info about about a specific service                                                 │
│ stats    Retrieve stats about a port                                                              │
│ top      Retrieve list of ports by frequency (TCP, UDP, SCTP or all of them. Defaults to 'all')   │
│ update   Update ports list                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```

This is the help for the ``topmostp top`` command:
```
 Usage: topmostp top [OPTIONS] N                                              
                                                                              
 Retrieve list of ports by frequency (TCP, UDP, SCTP or all of them. Defaults 
 to 'all')                                                                    
                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────╮
│ *    n      INTEGER  [default: None] [required]                            │
╰────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────╮
│ --type    -t      [tcp|udp|sctp|all]  [default: all]                       │
│ --silent  -s                          Display only results in output       │
│ --help    -h                          Show this message and exit.          │
╰────────────────────────────────────────────────────────────────────────────╯
```

This is the help for the ``topmostp find`` command:
```
 Usage: topmostp find [OPTIONS] SERVICE                                       
                                                                              
 Find info about about a specific service                                     
                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────╮
│ *    service      TEXT  [default: None] [required]                         │
╰────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                              │
╰────────────────────────────────────────────────────────────────────────────╯
```

This is the help for the ``topmostp stats`` command:
```
 Usage: topmostp stats [OPTIONS] PORT PORT_TYPE:{tcp|udp|sctp}                
                                                                              
 Retrieve stats about a port                                                  
                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────╮
│ *    port           INTEGER                   [default: None] [required]   │
│ *    port_type      PORT_TYPE:{tcp|udp|sctp}  [default: None] [required]   │
╰────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                              │
╰────────────────────────────────────────────────────────────────────────────╯
```

A pratical example is the following:
```
naabu -p $(topmostp top 15 -s) -host secsi.io
```

In this snippet the output of ``topmostp`` is used to retrieve the list of the top 15 ports and it is chained with the ``naabu`` port scanning tool.


## Demo
[![demo](https://asciinema.org/a/532210.svg)](https://asciinema.org/a/532210?autoplay=1)

## Credits
Developed by Angelo Delicato [@SecSI](https://secsi.io)

## License
*topmostp* is released under the [MIT LICENSE](https://github.com/cybersecsi/topmostp/blob/main/LICENSE.md)