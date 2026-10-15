from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import AsyncNinjaJWTDefaultController

api = NinjaExtraAPI()
api.register_controllers(AsyncNinjaJWTDefaultController)    
