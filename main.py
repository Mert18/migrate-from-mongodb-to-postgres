import psycopg2
from config import config
from datetime import datetime, timedelta
import pymongo
import uuid


# connection for database postgresql
connPostgres = None
try:
    # read database connection parameters
    params = config()
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    connPostgres = psycopg2.connect(**params)	
    # create a cursor to execute commands
    cur = connPostgres.cursor()

    myclient = pymongo.MongoClient("URL")
    mydb = myclient["words"]
    mycol = mydb["words"]
    cursor = mycol.find({})
    for document in cursor:
          myuuid = uuid.uuid4()
          cur.execute('INSERT INTO words(id, title, kind, difficulty) VALUES(%s, %s, %s, %s)', (str(myuuid), document['title'], document['kind'], "medium"))
          for description in document['description']:
              cur.execute('INSERT INTO word_descriptions(word_id, descriptions) VALUES(%s, %s)', (str(myuuid) , description))
          
          for synonym in document['synonyms']:
              cur.execute('INSERT INTO word_synonyms(word_id, synonyms) VALUES(%s, %s)', (str(myuuid) , synonym))
         
          for antonym in document['antonyms']:
               cur.execute('INSERT INTO word_antonyms(word_id, antonyms) VALUES(%s, %s)', (str(myuuid) , antonym))

          for sentence in document['sentences']:
               cur.execute('INSERT INTO word_sentences(word_id, sentences) VALUES(%s, %s)', (str(myuuid) , sentence))

    # commit the changes to the database
    connPostgres.commit()
    # close the communication with the PostgreSQL
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connPostgres is not None:
        connPostgres.close()
        print('Database connection closed.')
