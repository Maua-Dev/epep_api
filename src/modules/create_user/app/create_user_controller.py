from pydantic import ValidationError

from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_user_usecase import CreateUserUsecase
from .create_user_viewmodel import CreateUserViewmodel


from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Created

from src.shared.domain.enums.role_enum import RoleEnum


class CreateUserController:

    def __init__(self, usecase: CreateUserUsecase):
        self.CreateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')
            if request.data.get('password_hash') is None:
                raise MissingParameters('password_hash')

            user = self.CreateUserUsecase(
                email=request.data.get('email'),
                password_hash=request.data.get('password_hash'),
                role=request.data.get('role') or RoleEnum.USER
            )

            viewmodel = CreateUserViewmodel(user)

            return Created(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)
        
        except ValidationError as err:
            error = err.errors()[0]

            if error['loc'][0] == "email":
                return BadRequest(body="Field email is not valid")
            if error['loc'][0] == "password_hash":
                return BadRequest(body="Field password_hash is not valid")
            
            return BadRequest(body="Invalid data")

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
