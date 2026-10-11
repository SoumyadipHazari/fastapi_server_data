from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Keep q-fastapi.csv in the project root.
DATA_PATH = Path(__file__).resolve().parent.parent / "q-fastapi.csv"

with open(DATA_PATH, "r", encoding="utf-8", newline="") as f:
    students = [
        {
            "studentId": int(row["studentId"]),
            "class": row["class"],
        }
        for row in csv.DictReader(f)
    ]


@app.get("/api")
async def get_students(
    class_: list[str] | None = Query(default=None, alias="class")
):
    if class_:
        selected_classes = set(class_)
        filtered = [
            student for student in students
            if student["class"] in selected_classes
        ]
    else:
        filtered = students

    return {"students": filtered}
