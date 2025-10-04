from fastapi import APIRouter, Depends, Cookie, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserHistoryResponse
from app.utils.password_and_token import get_current_user
import aiofiles

router = APIRouter()


@router.post("/uploadfile/", response_model=UserHistoryResponse)
async def upload_file(file: UploadFile, access_token: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    user_id = get_current_user(access_token)
    if not file.filename.endswith((".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

    file_path = f"uploaded_files/{file.filename}"
    async with aiofiles.open(file_path, "wb") as f:
        context = await file.read()
        await f.write(context)

    """     ждем антона

    convertated_text = тут будет функция конвертации взятая из utils(которую я и жду)

    new_record = UserHistory(user_id=user_id, file_name=file.filename, text_result=convertated_text)

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record
    """
