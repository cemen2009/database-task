import os
import logging
from pymongo import MongoClient


logging.basicConfig(level=logging.INFO)

host = os.environ.get("MONGO_HOST", "mongo")
port = int(os.environ.get("MONGO_PORT", 27017))
user = os.environ.get("MONGO_USER", "admin")
password = os.environ.get("MONGO_PASSWORD", "secret")
db_name = os.environ.get("MONGO_DB", "mydatabase")

uri = f"mongodb://{user}:{password}@{host}:{port}/"
client = MongoClient(uri)
db = client[db_name]

conferences = [
  {
    "name": "International AI Conference 2025",
    "period": {
      "start": "2025-11-01",
      "end": "2025-11-03"
    },
    "building": "Tech Hall A",
    "sections": [
      {
        "title": "Machine Learning Advances",
        "number": 1,
        "presiding": "Dr. Alice Smith",
        "room": "101",
        "speech": [
          {
            "topic": "Deep Learning in Medicine",
            "date": "2025-11-01",
            "start_time": "09:00",
            "duration": "1h30m",
            "speaker": {
              "name": "Dr. John Doe",
              "degree": "PhD",
              "workplace": "University of Health Tech",
              "job_title": "Professor",
              "bio": "Specializes in AI applications in healthcare."
            },
            "equipment": [
              {"name": "Projector", "quantity": 1},
              {"name": "Microphone", "quantity": 2}
            ]
          }
        ]
      }
    ]
  },
  {
    "name": "Cybersecurity Summit 2025",
    "period": {
      "start": "2025-12-05",
      "end": "2025-12-07"
    },
    "building": "Security Center B",
    "sections": [
      {
        "title": "Network Security",
        "number": 1,
        "presiding": "Mr. Robert Lee",
        "room": "202",
        "speech": [
          {
            "topic": "Next-Gen Firewalls",
            "date": "2025-12-05",
            "start_time": "10:00",
            "duration": "2h",
            "speaker": {
              "name": "Ms. Laura Chen",
              "degree": "MSc",
              "workplace": "CyberTech Corp",
              "job_title": "Security Analyst",
              "bio": "Expert in enterprise network security solutions."
            },
            "equipment": [
              {"name": "Whiteboard", "quantity": 1},
              {"name": "Laptop", "quantity": 1}
            ]
          }
        ]
      }
    ]
  },
  {
    "name": "Renewable Energy Forum 2025",
    "period": {
      "start": "2025-09-15",
      "end": "2025-09-17"
    },
    "building": "Green Hall C",
    "sections": [
      {
        "title": "Solar Energy Innovations",
        "number": 1,
        "presiding": "Dr. Emily Johnson",
        "room": "303",
        "speech": [
          {
            "topic": "Photovoltaic Efficiency Improvements",
            "date": "2025-09-15",
            "start_time": "11:00",
            "duration": "1h",
            "speaker": {
              "name": "Dr. Mark Evans",
              "degree": "PhD",
              "workplace": "SolarTech Labs",
              "job_title": "Lead Researcher",
              "bio": "Research focuses on high-efficiency solar panels."
            },
            "equipment": [
              {"name": "Projector", "quantity": 1},
              {"name": "Pointer", "quantity": 1}
            ]
          }
        ]
      }
    ]
  }
]

logging.info("Inserting data into MongoDB...")
db.conferences.insert_many(conferences)
logging.info("Data inserted successfully.")

for conf in db.conferences.find():
    logging.info(conf)
