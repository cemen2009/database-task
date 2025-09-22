import os
import logging
from pymongo import MongoClient
from datetime import datetime


logging.basicConfig(level=logging.INFO)

host = os.environ.get("MONGO_HOST", "mongo")
port = int(os.environ.get("MONGO_PORT", 27017))
user = os.environ.get("MONGO_USER", "admin")
password = os.environ.get("MONGO_PASSWORD", "secret")
db_name = os.environ.get("MONGO_DB", "mydatabase")

uri = f"mongodb://{user}:{password}@{host}:{port}/"
client = MongoClient(uri)
db = client[db_name]


# predefined reference collections
buildings = [
    {"_id": 1, "name": "Tech Hall A", "address": "123 AI St", "createdAt": datetime(2025, 1, 1)},
    {"_id": 2, "name": "Security Center B", "address": "456 Cyber Rd", "createdAt": datetime(2025, 1, 1)},
    {"_id": 3, "name": "Green Hall C", "address": "789 Solar Ave", "createdAt": datetime(2025, 1, 1)}
]

rooms = [
    {"_id": 1, "buildingId": 1, "name": "101", "capacity": 50, "features": ["Projector", "Microphone"]},
    {"_id": 2, "buildingId": 2, "name": "202", "capacity": 40, "features": ["Whiteboard", "Laptop"]},
    {"_id": 3, "buildingId": 3, "name": "303", "capacity": 60, "features": ["Projector", "Pointer"]}
]

speakers = [
    {"_id": 1, "fullName": "Dr. John Doe", "degree": "PhD", "workplace": "University of Health Tech", "position": "Professor", "bio": "Specializes in AI applications in healthcare.", "email": "jdoe@uht.edu", "phone": "123-456-7890"},
    {"_id": 2, "fullName": "Ms. Laura Chen", "degree": "MSc", "workplace": "CyberTech Corp", "position": "Security Analyst", "bio": "Expert in enterprise network security solutions.", "email": "lchen@cybertech.com", "phone": "234-567-8901"},
    {"_id": 3, "fullName": "Dr. Mark Evans", "degree": "PhD", "workplace": "SolarTech Labs", "position": "Lead Researcher", "bio": "Research focuses on high-efficiency solar panels.", "email": "mevans@solartech.com", "phone": "345-678-9012"}
]

equipment_types = [
    {"_id": 1, "name": "Projector", "description": "HD Projector", "quantityAvailable": 10},
    {"_id": 2, "name": "Microphone", "description": "Wireless mic", "quantityAvailable": 20},
    {"_id": 3, "name": "Whiteboard", "description": "Magnetic whiteboard", "quantityAvailable": 5},
    {"_id": 4, "name": "Laptop", "description": "Presentation laptop", "quantityAvailable": 8},
    {"_id": 5, "name": "Pointer", "description": "Laser pointer", "quantityAvailable": 15}
]

conferences = [
    {
        "title": "International AI Conference 2025",
        "period_start": datetime(2025, 11, 1),
        "period_end": datetime(2025, 11, 3),
        "buildingId": 1,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "sections": [
            {
                "title": "Machine Learning Advances",
                "number": 1,
                "chairId": 1,
                "roomId": 1,
                "talks": [
                    {
                        "title": "Deep Learning in Medicine",
                        "start": datetime(2025, 11, 1, 9, 0),
                        "end": datetime(2025, 11, 1, 10, 30),
                        "speakerId": 1,
                        "roomId": 1,
                        "equipments": [
                            {"equipmentTypeId": 1, "qty": 1},
                            {"equipmentTypeId": 2, "qty": 2}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "title": "Cybersecurity Summit 2025",
        "period_start": datetime(2025, 12, 5),
        "period_end": datetime(2025, 12, 7),
        "buildingId": 2,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "sections": [
            {
                "title": "Network Security",
                "number": 1,
                "chairId": 2,
                "roomId": 2,
                "talks": [
                    {
                        "title": "Next-Gen Firewalls",
                        "start": datetime(2025, 12, 5, 10, 0),
                        "end": datetime(2025, 12, 5, 12, 0),
                        "speakerId": 2,
                        "roomId": 2,
                        "equipments": [
                            {"equipmentTypeId": 3, "qty": 1},
                            {"equipmentTypeId": 4, "qty": 1}
                        ]
                    }
                ]
            }
        ]
    },
    {
        "title": "Renewable Energy Forum 2025",
        "period_start": datetime(2025, 9, 15),
        "period_end": datetime(2025, 9, 17),
        "buildingId": 3,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "sections": [
            {
                "title": "Solar Energy Innovations",
                "number": 1,
                "chairId": 3,
                "roomId": 3,
                "talks": [
                    {
                        "title": "Photovoltaic Efficiency Improvements",
                        "start": datetime(2025, 9, 15, 11, 0),
                        "end": datetime(2025, 9, 15, 12, 0),
                        "speakerId": 3,
                        "roomId": 3,
                        "equipments": [
                            {"equipmentTypeId": 1, "qty": 1},
                            {"equipmentTypeId": 5, "qty": 1}
                        ]
                    }
                ]
            }
        ]
    }
]


# reference collections first
db.buildings.insert_many(buildings)
db.rooms.insert_many(rooms)
db.speakers.insert_many(speakers)
db.equipmentTypes.insert_many(equipment_types)

# insert conferences with embedded sections, talks, and equipment
logging.info("Inserting conferences into MongoDB...")
db.conferences.insert_many(conferences)
logging.info("Data inserted successfully.")

for conf in db.conferences.find():
    logging.info(conf)
