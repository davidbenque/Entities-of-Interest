#SOS.BSD. LTD
Status: Defaulted
Address: SHECHTER JAKOV ISRAEL 11 HAALIYA HASHNIYA, BNIE-BRAK ISRAEL

##Incoming
BENEFICIARY
Mr SHECHTER JAKOV
Israel


SHAREHOLDER
Lilay LTD
Anguilla


INTERMEDIARY
SHECHTER JAKOV ISRAEL
Israel



##Graph
```mermaid
graph LR
classDef outline fill:#fff,stroke:#000,stroke-width:1px;
node1[SOSBSD LTD<br>]
node2[Mr SHECHTER JAKOV<br>Israel]
node2-->|BENEFICIARY_OF|node1
node3[Lilay LTD<br>Anguilla]
node3-->|SHAREHOLDER_OF|node1
node4[SHECHTER JAKOV ISRAEL<br>Israel]
node4-->|INTERMEDIARY_OF|node1
class node1 outline
node2-->|BENEFICIARY_OF|node1
node5[<br>Israel]
node2-->|REGISTERED_ADDRESS|node5
node6[<br>Anguilla]
node3-->|REGISTERED_ADDRESS|node6
node7[Tribeca Marketing Ltd<br>]
node3-->|SHAREHOLDER_OF|node7
node8[Fxcapital LTD<br>]
node3-->|SHAREHOLDER_OF|node8
node3-->|SHAREHOLDER_OF|node1
node9[Simple Care LTD<br>]
node4-->|INTERMEDIARY_OF|node9
node4-->|INTERMEDIARY_OF|node1
node10[Avitan Minerals Ltd<br>]
node4-->|INTERMEDIARY_OF|node10
node11[NC International LTD<br>]
node4-->|INTERMEDIARY_OF|node11
```