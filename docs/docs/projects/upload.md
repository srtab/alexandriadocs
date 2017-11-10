# Upload documentation

## Using `curl`

```shell
$ curl -X POST -H "Content-Type: multipart/form-data" -H "Authorization: Token 51ab06e0ea051d4e9a5c3c3ef743d4fbfda018f8" -F "project=1" -F "archive=@project.tar.gz" https://alexandriadocs.io/api/v1/projects/upload/
```
