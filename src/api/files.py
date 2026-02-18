from fastapi import APIRouter, UploadFile

router = APIRouter()

@router.post("/files")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"1_{filename}", "wb") as f:
        f.write(file.read())
    return {"file": filename}