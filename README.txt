Eda Özyılmaz 2171882
Hilal Ünal 2172112

STEPS:

1. Connect each node with ssh using commands:
    for node d: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2171882@pc2.instageni.maxgigapop.net -p 29610
    for node r1: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2171882@pc2.instageni.maxgigapop.net -p 29611
    for node r2: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2171882@pc2.instageni.maxgigapop.net -p 29612
    for node r3: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2171882@pc2.instageni.maxgigapop.net -p 29613
    for node s: $ ssh -i ~/.ssh/id_geni_ssh_rsa e2171882@pc2.instageni.maxgigapop.net -p 29614

2. For each node, copy the corresponding files to machines. Also for node s copy input.txt and input2.txt to machines.

3. For "experiment1" part run the scripts on following order:
     $ python d.py 1
     $ python r3.py
     $ python s.py 1

4. After experiment1 is over, it created text that contains input file:
      for d: output1.txt

5. For "experiment2" part run the scripts on following order:
     $ python d.py 2
     $ python r1.py
     $ python r2.py
     $ python s.py 2

6. After experiment2 is over, it created text that contains input file:
      for d: output2.txt

7. For all the parts of the "experimental result" first do:
    a. For experiment 1 with 5% loss:
     for node s:
		   $ sudo tc qdisc add dev eth2 root netem loss 5% delay 3ms #conection between s-r3
     for node r3:
		   $ sudo tc qdisc add dev eth3 root netem loss 5% delay 3ms  #conection between r3-s
                   $ sudo tc qdisc add dev eth2 root netem loss 5% delay 3ms  #conection between r3-d
     for node d:
	           $ sudo tc qdisc add dev eth3 root netem loss 5% delay 3ms  #conection between d-r3
    b. For experiment 1 with 15% loss:
     for node s:
		   $ sudo tc qdisc change dev eth2 root netem loss 15% delay 3ms #conection between s-r3
     for node r3:
		   $ sudo tc qdisc change dev eth3 root netem loss 15% delay 3ms  #conection between r3-s
                   $ sudo tc qdisc change dev eth2 root netem loss 15% delay 3ms  #conection between r3-d
     for node d:
	           $ sudo tc qdisc change dev eth3 root netem loss 15% delay 3ms  #conection between d-r3
    c. For experiment 1 with 38% loss:
     for node s:
		   $ sudo tc qdisc change dev eth2 root netem loss 38% delay 3ms #conection between s-r3
     for node r3:
		   $ sudo tc qdisc change dev eth3 root netem loss 38% delay 3ms  #conection between r3-s
                   $ sudo tc qdisc change dev eth2 root netem loss 38% delay 3ms  #conection between r3-d
     for node d:
	           $ sudo tc qdisc change dev eth3 root netem loss 38% delay 3ms  #conection between d-r3

    d. For experiment 2 with 5% loss:
     for node s:
		   $ sudo tc qdisc add dev eth3 root netem loss 5% delay 3ms #conection between s-r1
                   $ sudo tc qdisc add dev eth1 root netem loss 5% delay 3ms #conection between s-r2
     for node r1:
		   $ sudo tc qdisc add dev eth3 root netem loss 5% delay 3ms  #conection between r1-s
                   $ sudo tc qdisc add dev eth2 root netem loss 5% delay 3ms  #conection between r1-d
     for node r2:
		   $ sudo tc qdisc add dev eth4 root netem loss 5% delay 3ms  #conection between r2-s
                   $ sudo tc qdisc add dev eth3 root netem loss 5% delay 3ms  #conection between r2-d
     for node d:
	           $ sudo tc qdisc add dev eth1 root netem loss 5% delay 3ms  #conection between d-r1
                   $ sudo tc qdisc add dev eth3 root netem loss 5% delay 3ms  #conection between d-r2
    e. For experiment 2 with 15% loss:
     for node s:
		   $ sudo tc qdisc change dev eth3 root netem loss 15% delay 3ms #conection between s-r1
                   $ sudo tc qdisc change dev eth1 root netem loss 15% delay 3ms #conection between s-r2
     for node r1:
		   $ sudo tc qdisc change dev eth3 root netem loss 15% delay 3ms  #conection between r1-s
                   $ sudo tc qdisc change dev eth2 root netem loss 15% delay 3ms  #conection between r1-d
     for node r2:
		   $ sudo tc qdisc change dev eth4 root netem loss 15% delay 3ms  #conection between r2-s
                   $ sudo tc qdisc change dev eth3 root netem loss 15% delay 3ms  #conection between r2-d
     for node d:
	           $ sudo tc qdisc change dev eth1 root netem loss 15% delay 3ms  #conection between d-r1
                   $ sudo tc qdisc change dev eth3 root netem loss 15% delay 3ms  #conection between d-r2
    f. For experiment 2 with 38% loss:
     for node s:
		   $ sudo tc qdisc change dev eth3 root netem loss 38% delay 3ms #conection between s-r1
                   $ sudo tc qdisc change dev eth1 root netem loss 38% delay 3ms #conection between s-r2
     for node r1
		   $ sudo tc qdisc change dev eth3 root netem loss 38% delay 3ms  #conection between r1-s
                   $ sudo tc qdisc change dev eth2 root netem loss 38% delay 3ms  #conection between r1-d
     for node r2:
		   $ sudo tc qdisc change dev eth4 root netem loss 38% delay 3ms  #conection between r2-s
                   $ sudo tc qdisc change dev eth3 root netem loss 38% delay 3ms  #conection between r2-d
     for node d:
	           $ sudo tc qdisc change dev eth1 root netem loss 38% delay 3ms  #conection between d-r1
                   $ sudo tc qdisc change dev eth3 root netem loss 38% delay 3ms  #conection between d-r2

