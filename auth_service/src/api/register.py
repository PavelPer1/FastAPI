import os
from fastapi import APIRouter, UploadFile, HTTPException
from openpyxl import load_workbook
from sqlalchemy.exc import IntegrityError
from auth_service.src.models.crud import register_user, get_user_by_username  # Добавьте эту функцию

router = APIRouter()


@router.post("/register-from-excel-with-email")
async def register_from_excel_with_email(file: UploadFile):
    """
    Загружает Excel файл с данными пользователей и регистрирует их.
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, "Файл должен быть в формате Excel")

    os.makedirs("users_files", exist_ok=True)
    file_path = f"users_files/{file.filename}"

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        workbook = load_workbook(file_path)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[1] if cell.value]

        if 'username' not in headers:
            raise HTTPException(400, "В Excel файле отсутствует колонка: username")
        if 'password' not in headers:
            raise HTTPException(400, "В Excel файле отсутствует колонка: password")

        registered_users = []
        skipped_users = []  # Новый список для пропущенных (уже существующих)
        failed_users = []

        username_idx = headers.index('username')
        password_idx = headers.index('password')
        email_idx = headers.index('email') if 'email' in headers else None

        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), 2):
            if not any(row):
                continue

            try:
                username = str(row[username_idx]) if row[username_idx] else None
                password = str(row[password_idx]) if row[password_idx] else None

                if not username:
                    raise ValueError("Username не может быть пустым")
                if not password:
                    raise ValueError("Password не может быть пустым")

                # 1. Проверяем, существует ли пользователь
                existing_user = await get_user_by_username(username)

                if existing_user:
                    # Пользователь уже есть - пропускаем, но не считаем ошибкой
                    skipped_users.append({
                        "row": row_idx,
                        "username": username,
                        "reason": "User already exists"
                    })
                    continue

                # 2. Если не существует - регистрируем
                await register_user(
                    username=username,
                    password=password
                )

                user_info = {
                    "row": row_idx,
                    "username": username,
                    "status": "success"
                }

                if email_idx is not None and row[email_idx]:
                    user_info["email"] = str(row[email_idx])

                registered_users.append(user_info)

            except IntegrityError as e:
                # Ловим специфическую ошибку целостности БД
                if "duplicate key" in str(e).lower():
                    skipped_users.append({
                        "row": row_idx,
                        "username": username if username else "Unknown",
                        "reason": "User already exists (caught by IntegrityError)"
                    })
                else:
                    failed_users.append({
                        "row": row_idx,
                        "username": username if username else "Unknown",
                        "error": f"Database integrity error: {str(e)[:200]}"
                    })
            except Exception as e:
                failed_users.append({
                    "row": row_idx,
                    "username": username if username else "Unknown",
                    "error": str(e)
                })

        if os.path.exists(file_path):
            os.remove(file_path)

        total_processed = len(registered_users) + len(skipped_users) + len(failed_users)
        return {
            "success": len(failed_users) == 0,
            "message": f"Новых: {len(registered_users)}, Пропущено (уже есть): {len(skipped_users)}, Ошибок: {len(failed_users)}",
            "registered_users": registered_users,
            "skipped_users": skipped_users,  # Теперь видно, кого пропустили
            "failed_users": failed_users,
            "statistics": {
                "total_processed": total_processed,
                "new_registrations": len(registered_users),
                "already_existed": len(skipped_users),
                "errors": len(failed_users),
                "success_rate": f"{(len(registered_users) / total_processed * 100):.1f}%" if total_processed > 0 else "0%"
            }
        }

    except HTTPException:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(500, f"Ошибка при обработке файла: {str(e)}")