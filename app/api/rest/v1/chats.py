from fastapi import APIRouter

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/")
def create_chat():
    pass


@router.get("/")
def get_all_chats():
    pass


@router.get("/{chat_id}")
def get_chat(chat_id: int):
    pass
