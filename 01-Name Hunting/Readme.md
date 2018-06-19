# 01-Name Hunting

The ICIJ database can be downloaded [here](https://offshoreleaks.icij.org/pages/database) (scroll down for the Neo4j Desktop executable).

#### Example Cypher Queries


Query with offset used to extract the names

`match (e:Entity) return e.name, e.internal_id skip 12000 limit 1000`

Results from 00000 to 12000 have been exported as .csv files in `/Batch 00000 - 12000/`.


older queries:

```
match (e:Entity) return e.name, e.status, e.incorporation_date, e.inactivation_date, e.countries, e.jurisdiction_description, e.service_provider limit 1000
```

```
match (e:Entity {status:"Defaulted"}) return e.name, e.status, e.incorporation_date, e.inactivation_date, e.countries, e.jurisdiction_description, rand() as r
order by r
limit 1000
```

Match multiple property values

```
MATCH (e:Entity) WHERE e.status IN ['Dead', 'Inactive', 'Defaulted', 'Struck / Defunct / Deregistered']
```

```
return e.name, e.status, e.incorporation_date, e.inactivation_date, e.countries, e.jurisdiction_description, rand() as r
order by r
limit 1000
```


