#MOONDUST SERVICES LIMITED
Status: Defaulted
Address: DENNIS M HILL C.ACCS [Mr Dennis Hill] High Pines Blackdown Avenue Pyrford,Woking SURREY GU22 8QG

##Incoming
SHAREHOLDER
MALCOLM JOHN HUSE
United Arab Emirates


SHAREHOLDER
DEE CORCORAN
United Arab Emirates


INTERMEDIARY
DENNIS M HILL C.ACCS
United Kingdom



##Graph
```mermaid
graph LR
classDef outline fill:#fff,stroke:#000,stroke-width:1px;
node1[MOONDUST SERVICES LIMITED<br>]
node2[MALCOLM JOHN HUSE<br>United Arab Emirates]
node2-->|SHAREHOLDER_OF|node1
node3[DEE CORCORAN<br>United Arab Emirates]
node3-->|SHAREHOLDER_OF|node1
node4[DENNIS M HILL CACCS<br>United Kingdom]
node4-->|INTERMEDIARY_OF|node1
class node1 outline
node5[<br>United Arab Emirates]
node2-->|REGISTERED_ADDRESS|node5
node2-->|SHAREHOLDER_OF|node1
node3-->|REGISTERED_ADDRESS|node5
node3-->|SHAREHOLDER_OF|node1
node6[Access Group International Limited<br>]
node4-->|INTERMEDIARY_OF|node6
node4-->|INTERMEDIARY_OF|node1
node7[ALBERT JACK LIMITED<br>]
node4-->|INTERMEDIARY_OF|node7
```