# Embedded Design: Conference System

## Class Diagram

```mermaid
classDiagram
  class Building {
    ObjectId _id
    string name
    string address
    date createdAt
  }

  class Room {
    ObjectId _id
    ObjectId buildingId
    string name
    int capacity
    string[] features
  }

  class Conference {
    ObjectId _id
    string title
    date period_start
    date period_end
    ObjectId buildingId
    date createdAt
    date updatedAt
    Section[] sections
  }

  class Section {
    ObjectId _id
    string title
    int number
    ObjectId chairId
    ObjectId roomId
    Talk[] talks
  }

  class Talk {
    ObjectId _id
    ObjectId roomId
    ObjectId speakerId
    string title
    date start
    date end
    TalkEquipment[] equipments
  }

  class TalkEquipment {
    ObjectId equipmentTypeId
    int qty
  }

  class Speaker {
    ObjectId _id
    string fullName
    string degree
    string workplace
    string position
    string bio
    string email
    string phone
  }

  class EquipmentType {
    ObjectId _id
    string name
    string description
    int quantityAvailable
  }

  %% Embedding (composition) & references (aggregation)
  Conference "1" *-- "many" Section : embeds
  Section "1" *-- "many" Talk : embeds
  Talk "1" *-- "many" TalkEquipment : embeds

  Conference "1" o-- "1" Building : located_at
  Section "1" o-- "1" Room : held_in
  Section "1" o-- "1" Speaker : chaired_by
  Talk "1" o-- "1" Room : in_room
  Talk "1" o-- "1" Speaker : given_by
  TalkEquipment "many" o-- "1" EquipmentType : type
```

## Notes

- ``TalkEquipment`` represents the ``talks.equipment[]`` embedded array (logical associative entity).
- ``Conferences.period_start`` / ``period_end`` are flattened for indexing; original nested period can be stored and projected as needed.
- Denormalized fields on ``Talk`` (conferenceId, roomId) improve schedule queries and reporting.

## Suggested Key Indexes

- Talks: ``{ conferenceId: 1, start: 1 }``, ``{ roomId: 1, start: 1, end: 1 }``, ``{ speakerId: 1, start: 1, end: 1 }``, ``{ "equipment.equipmentTypeId": 1 }``
- Sections: ``{ conferenceId: 1, number: 1 } (unique), { roomId: 1 }``, ``{ chairId: 1 }``
- Rooms: ``{ buildingId: 1, name: 1 } (unique within building)``
- Conferences: ``{ period_start: 1, period_end: 1 }``, ``{ buildingId: 1 }``