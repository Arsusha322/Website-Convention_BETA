from fastapi import APIRouter, Depends, Cookie, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserHistory
from app.schemas import UserHistoryCreate, UserHistoryResponse
from app.utils import get_current_user

router = APIRouter()


@router.post("/uploadfile/", response_model=UserHistoryResponse)
def upload_file(file: UploadFile, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    if not file.filename.endswith((".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

    file_path = f"uploaded_files/{file.filename}"
    with open(file_path, "wb") as f:
        context = file.read()
        f.write(context)

    """     ждем антона

    convertated_text = тут будет функция конвертации взятая из utils(которую я и жду)

    new_record = UserHistory(user_id=user_id, file_name=file.filename, text_result=convertated_text)

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record
    """
