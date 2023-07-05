RDS, DynamoDB, EC2 and ECS.

## metadata scraper
# scrape
Develop a metadata scraper in Golang or Python that retrieves information from the
provided list of IPFS CIDs. The scraper should fetch details like:

```JSON
{
"image": "string",
"description": "string",
"name": "string"
}
```

Requirements
- config list of IPFS CIDs
- curl https://blockpartyplatform.mypinata.cloud/ipfs/<CID>
- parse and filter data
- build data objects from curl
- 

# sync to RDS
Use an AWS SDK in your Golang / Python service to connect to a DynamoDB (or RDS)
instance and store the scraped data.

Requirements
- connect to database
- sync objects to database

# Retrieve Data
Set up a Golang-based RESTful API with the following endpoints:
● GET /tokens: This endpoint should fetch all data stored in the database and return it in
JSON format.
● GET /tokens/<cid>: This endpoint should fetch only the one record for that individual
IPFS cid

Requirements
- 