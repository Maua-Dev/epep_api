from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_member_usecase import CreateMemberUsecase
from .create_member_viewmodel import CreateMemberViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Created


class CreateMemberController:

    def __init__(self, usecase: CreateMemberUsecase):
        self.CreateMemberUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('name') is None:
                raise MissingParameters('name')

            if request.data.get('function') is None:
                raise MissingParameters('function')

            if request.data.get('linkedin') is None:
                raise MissingParameters('linkedin')

            if request.data.get('photo') is None:
                raise MissingParameters('photo')

            if request.data.get('description') is None:
                raise MissingParameters('description')

            member = self.CreateMemberUsecase(
                name=request.data.get('name'),
                function=request.data.get('function'),
                linkedin=request.data.get('linkedin'),
                photo=request.data.get('photo'),
                description=request.data.get('description')
            )

            viewmodel = CreateMemberViewmodel(member)

            return Created(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
