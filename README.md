# Intro
    TODO

### Directory structures
    ├── cfgs
    │   ├── demo.pickle
	│   ├── syringe_pump.pickle
    │   ├── temperature.pickle
	│   └── ultra.pickle
	├── logs
	│   ├── demo-buffer-overflow
	│   │   └── combined.cflog
	│   ├── demo-valid-cf
	│   │   └── combined.cflog
	│   ├── other_demo
	│   │   ├── pruned_10.cflog
	│   │   ├── pruned_100.cflog
    │   │   ├── pruned_1000.cflog
    │   │   ├── pruned_1000000.cflog
	│   │   ├── pruned_10000000.cflog
    │   │   ├── regular1.cflog
    │   │   ├── regular2.cflog
	│   │   ├── regular3.cflog
	│   │   └── regular4.cflog
	│   ├── pump
	│   │   ├── pruned_10.cflog
	│   │   ├── pruned_100.cflog
    │   │   ├── pruned_1000.cflog
    │   │   ├── pruned_1000000.cflog
	│   │   ├── pruned_10000000.cflog
    │   │   ├── regular1.cflog
    │   │   ├── regular2.cflog
	│   │   └── regular3.cflog
	│   ├── temperature
	│   │   ├── pruned_10.cflog
	│   │   ├── pruned_100.cflog
    │   │   ├── pruned_1000.cflog
    │   │   ├── pruned_1000000.cflog
	│   │   ├── pruned_10000000.cflog
    │   │   ├── regular1.cflog
    │   │   ├── regular2.cflog
	│   │   └── regular3.cflog
	│   └── ultra
	│   │   ├── pruned_10.cflog
	│   │   ├── pruned_100.cflog
    │   │   ├── pruned_1000.cflog
    │   │   ├── pruned_1000000.cflog
	│   │   ├── pruned_10000000.cflog
    │   │   ├── regular1.cflog
    │   │   ├── regular2.cflog
	│   │   └── regular3.cflog
	├── project
	│   ├── pruning_files
    │   │   ├── demo.txt
    │   │   ├── syringe_pump.txt
    │   │   ├── temperature.txt
    |   |   └── ultra.txt
	│   ├── log_generator.py
	│   ├── project.py
	│   └── structures.py

## CFGs
The cfgs directory stores the Control Flow Graphs of four sample programs. demo.pckle represents a simple user authentication program. Syringe_pump.pickle was generated from a
microcontroller controlled medical syringe. Finally temperature.pickle and ultra.pickle represent a temperature and ultra sonic sensor respectively. All programs were 
designed for microcontrollers and are vulnerable to some form of runtime attack. A CFG is a directed graph in which each node represents an atomic unit of code. 
That is to say that each node represents a section of the binary that is always executed in order. Each node ends with a branching instruction 
(i.e. call, return, jump, if, etc.) These branching instructions are able to jump through out memory however during normal execution branching instructions 
have a finite set of valid destinations represented by the directed connections of the graph. DUe to this CFGs allow us to enumerate correct paths through a binary

## Logs
The log directory contains sample control flow logs to test the verifier with. The demo-buffer-overflow and demo-verifier-cf contian logs generated from tests of 
the Control Flow Attestation (CFA) scheme ACFA which motivated this project. The remaining directories represent logs generated for testing puropes. These remaining 
directories due represent valid paths in the binaries however they are not idicative of actual binary executions. This is due to the small scale of the sample programs.
Under normal operation, the provided sample binaries would generate around 75 log entries at most with the majority of logs being much less. As such we needed to create
non-realistic logs to generate larger workloads for better testing and comparisons. Each of these remaining directories contain 3 types of logs.

#### regularx.cflog
These logs represent more realistic executions of the binary. While not 100% accurate these logs were generated by choosing a random node in the CFG to start at and
traversing the graph until either n log entries were generated of execution reached a sink. For the traversal, we randomly chose from one the nodes valid successors 
for the next node to process. This random pathing also allowed us to generate paths thorough smaller portions of the binary not normally reachbale by normal execution

#### pruned_x.cflog
Pruned logs represent bulk data. Unlike regular logs, the x in pruned logs' names represents the number of log entries in the file. To generate these logs without ending
in a sink and repeating that same entry for the majority of the log, we prune the CFG (hence the name). Before generating the log, we remove all nodes that lead to a sink.
This allows for the log entries to be more varied, mimicing a larger program/run even if it there really are only a handful of possible paths.

#### overflowx.cflog
    TODO

## Generating Logs
To generate these logs we use log_generator.py. To simply create a regular log run:

    python log_generator -c "cfg-file" -e n
    
where "cfg-file" is the path to the cfg of the binary you want to use and n is the number of entries you want to generate. The -o flag can also be used to specify
the name and loctaion of the resulting log file. If unspecified the generated log will be stored in the current directoy as log.cflog. When generating regular logs 
you may need to edit the resulting file to remove repeated end entries as sinks will just fill the remainder of the log with the same value. Ultimately this is not \
needed as these loops are valid paths so verification should succede either way.

To generate pruned logs you also need to include the path to a pruning file. This can be done as follows:

    python log_generator -c "cfg-file" -e n -p "pruning-file"

The pruning files are stored in the project/pruning_files directory.

To make an overflow log simply take either a regular or pruned log and edit any entry. This change will represent an invalid control flow such as return oriented program.

The -h option can be used to get more information about the available command line flags

## Verifing Logs
TODO update when actual execution stabalizes

To verify that a log represents a correct execution of the binary simply run project.py as follows:

    python project.py "cfg-file" "log-file" name
    
where cfg-file is the cfg of the program the log represents, log-file is the log to be verified, and n is the number of threads to use for the verification. To verify the 
log, the program splits the log into n sections and gives each section to a thread. Each thread runs through its portion verifiying that the source address is the end appropriate end address of the node jumped to in the previous entry, the source address is a valid branching instruction, and the destination is a valid destination for the source address. Each log portion, excpet the final portion, actually contian (log_size/n) + 1 entries. This creates a single entry of overlap between the threads data allowing us to verify the correct execution across threads as well. Each thread stores the reuslts of their check in a shared list. If any thread detects an issue, it stores a 0 in the shared array. After all threads finished, the shared array is ANDed together to determine if the log represents a valid execution of the binary.