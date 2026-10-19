from typing import List

from src.shared.helpers.external_interfaces.external_interface import IRequest
from .get_all_members_usecase import GetAllMembersUsecase
from .get_all_members_viewmodel import GetAllMembersViewmodel
from src.shared.domain.entities.member import Member
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import NotFound, OK, BadRequest, InternalServerError


class GetAllMembersController:
    def __init__(self, usecase: GetAllMembersUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            all_members_list: List[Member] = self.usecase()

            viewmodel = GetAllMembersViewmodel(all_members_list)

            return OK(viewmodel.to_dict())

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
