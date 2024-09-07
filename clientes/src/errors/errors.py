class ApiError(Exception):
    code = 422
    description = "Default message"

class NotFound(ApiError):
    code = 404
    description = "No se encontro informacion con los campos enviados."

class ResourcesRequired(ApiError):
    code = 400
    description = "Hay algunos campos requeridos por favor valide."

class ResourcesAlreadyExist(ApiError):
    code = 412
    description = "El registro ya existe por favor valide."

class ExpiredInformation(ApiError):
    code = 401
    description = "La informacion que solicita ha expirado, considere autentificarse nuevamente."

class IncompleteRequest(ApiError):
    code = 403
    description = "No viene la informacion de autentificacion en la peticion."

class NotVerified(ApiError):
    code = 401
    description = "El usuario no paso la verificación."

class ToVerify(ApiError):
    code = 401
    description = "El usuario tiene la verificación pendiente."

class TimeOut(ApiError):
    code = 408
    description = "lo sentimos supero el tiempo."