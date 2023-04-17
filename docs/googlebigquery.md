## Little guide to download source code data from Github using Google Big Query

- Create a Google platform account (you will have around 300 $ given for free , that is sufficient for Github)
- Create a Google Big Query project
- In this project, create a dataset
- In this dataset, create one table per programming language. The results of each SQL request (one per language) will be stored in these tables.
- Before running your SQL request, make sure you change the query settings to save the query results in the dedicated table (more -> Query Settings -> Destination -> table for query results -> put table name)
- Run your SQL request (one per language and dont forget to change the table for each request)
- Export your results to google Cloud :
  - In google cloud storage, create a bucket and a folder per language into it
  - Export your table to this bucket ( EXPORT -> Export to GCS -> export format JSON , compression GZIP)
- To download the bucket on your machine, use the API gsutil:
  - pip install gsutil
  - gsutil config -> to config gsutil with your google account
  - gsutil -m cp -r gs://name_of_bucket/name_of_folder . -> copy your bucket on your machine

Example of query for python :
```
SELECT 
 f.repo_name,
 f.ref,
 f.path,
 c.copies,
 c.content
FROM `bigquery-public-data.github_repos.files` as f
  JOIN `bigquery-public-data.github_repos.contents` as c on f.id = c.id
WHERE 
  NOT c.binary
  AND f.path like '%.py'
```

Google link for more info here
