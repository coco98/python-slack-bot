import os
import sys

try:
   if os.environ["PRODUCTION"]:
      dataUrl = "http://data.hasura/v1/query"
      dataHeaders = {"Content-Type": "application/json", "X-Hasura-Role":"anonymous", "X-Hasura-User-Id":"0"}
except KeyError:
    dataUrl = "http://127.0.0.1:6432/v1/query"
    dataHeaders = {"Content-Type": "application/json", "X-Hasura-Role":"anonymous", "X-Hasura-User-Id":"0"}
