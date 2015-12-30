# Intrusion Detection

## Model builder

##Syscall Sequence Model
The model builder script takes in strace files. 
The strace files have process id and system calls (along with arguments passed to the system calls), the strace files are read one by one, each line is read, and all systems call functions are recorded as a list of cmd. 
From the initial sequence above, the resulting digram model would be:
(execve, brk)
(brk, access)
(access, mmap)
(mmap, access)
(access, open)
on running the python script:

./squence path of strace file

Program outputs the modal as JSON in following Format:
{
    "model": [
        {
            "syscall_1": "<first syscall>",
            "syscall_2": "<second syscall>"
        },
        // ...
    ]
}

##Augmented Syscall Sequence Model

A similar procedure is followed to record all the arguments as well. 
(execve ./prset03, brk)
(brk, access /etc/)
(access /etc/, mmap)
(mmap, access /etc/)
(access /etc/, open /etc/)
The calls which have paths as argument are collected together and for each the largest common path is computed. Merging digram entries by taking the longest common prefix between two strings
(brk, access /etc/ld.so.nohwcap)
(brk, access /etc/ld.so.cache)
the merge would be
(brk, access /etc/ld.so.)
JSON representation of the augmented initial sequence above after merging might be:

./model path of strace

Ex:
{
    "model": [
        {
            "syscall_1": "execve",
            "syscall_2": "brk",
            "syscall_1_arg": "./prset03",
            "syscall_2_arg": null
        },
        {
            "syscall_1": "brk",
            "syscall_2": "access",
            "syscall_1_arg": null,
            "syscall_2_arg": "/etc/"
        },
        {
            "syscall_1": "access",
            "syscall_2": "mmap",
            "syscall_1_arg": "/etc/",
            "syscall_2_arg": null
        },
        {
            "syscall_1": "mmap",
            "syscall_2": "access",
            "syscall_1_arg": null,
            "syscall_2_arg": "/etc/"
        },
        {
            "syscall_1": "access",
            "syscall_2": "open",
            "syscall_1_arg": "/etc/",
            "syscall_2_arg": "/etc/"
        }
    ]
}
##Mimicry attack questions.
There are two models built: 
one which has only the system calls, this is not a very efficient way of detection, as the exploit can be such that the system calls (consecutive pairs) it makes seems valid, like storing the shell script in an environmental variable and pointing the return address to location of environmental variable. 
First mimicry attack goes un-detected. 
When the argument of system call is also included in the comparison, the IDS becomes sounder as the arguments to system call in the exploit will vary and intrusion detected.
Second mimicry attack is detected.

##Enforcer:
First the strace is loaded and a list of cmds is extracted from strace and the solution.json is loaded. Pairs of system calls along with their arguments are compared against the suspect file, if there occurs any pair of consecutive systems calls which do not occur in the model then a malicious input has been detected. Comaparison happens if there is a match it is true else it false if it does not find anywhere.
Output Example:
$ ./checker /path/to/solution.json /path/to/strace_output
{
    "malicious": false,
    "syscall": null,
    "syscall_arg": null
}
