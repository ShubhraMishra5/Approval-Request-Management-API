from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return {"message" : "fastapi working"}

#  if request.approver_role != "MANAGER":
#         raise HTTPException(
#             status_code = 403,
#             detail = "only manager can approve"
#         )