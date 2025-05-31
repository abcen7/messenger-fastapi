TODO:
1) Monolith architecture
2) Redis
3) Docker
4) Soft delete for all models

USER FLOWS:
1) Chat with local person (User -> User):
   1) Create chat: `POST -> /api/v1/chats`
    params:
        - `title: str` (Name of the chat)
        - `type: "private"` (Type of the chat "private" | "group")
        - `user_id: int` (The id of person he wants to communicate with)
   2) Create row in table db `chats` (return `chat_id`)
   3) Create two rows in table db `chat_members` params:
        - `chat_id: int` (Created chat)
        - `user_id: int` (The id of person he wants to communicate with)

2) Chat with group (User -> Group):
   1) Create group: `POST -> /api/v1/groups`
    params:
        - `title: str` (Name of the chat)
        - `type: "local"` (Type of the chat "private" | "group")
        - `user_id: list[int]` (The ids of person he wants to communicate with)
   2) Create row in table db `chats` (return `chat_id`)
   3) Create `N` rows in table db `chat_members` params:
        - `chat_id: int` (Created chat)
        - `user_ids: int` (The ids of person he wants to communicate with)

Create the base realization of repository from Kirill's service with generics
