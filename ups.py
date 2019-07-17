import csv
import boto3
import uuid

def convert_csv_to_json_list(file):
   items = []
   with open(file) as csvfile:
      reader = csv.DictReader(csvfile, delimiter="\t")
      for row in reader:
          data = {}
          for i in range(1, 20):
              i = str(i)
              data[i] = row[i]
          data['id'] = str(uuid.uuid4())
          items.append(data)
   return items

def batch_write(items):
   dynamodb = boto3.resource('dynamodb')
   db = dynamodb.Table('ClaimFinder')

   with db.batch_writer() as batch:
      for item in items:
         batch.put_item(Item=item)

if __name__ == '__main__':
   json_data = convert_csv_to_json_list('dosya.tsv')
   batch_write(json_data)