# from ninja.router import Router
from ninja_extra.router import Router
from ninja_jwt.authentication import JWTAuth

router = Router()


@router.get("/", auth=JWTAuth())
def protected_endpoint(request):
  return {"message": "This is a protected endpoint."}
