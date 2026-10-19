from uuid import UUID
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_member_usecase import UpdateMemberUsecase
from .update_member_viewmodel import UpdateMemberViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class UpdateMemberController:

    def __init__(self, usecase: UpdateMemberUsecase):
        self.UpdateMemberUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('member_id') is None:
                raise MissingParameters('member_id')

            if not isinstance(request.data.get('member_id'), str):
                raise WrongTypeParameter(
                    fieldName="member_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('member_id').__class__.__name__
                )

            if request.data.get('new_name') is not None and not isinstance(request.data.get('new_name'), str):
                raise WrongTypeParameter(
                    fieldName="new_name",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_name').__class__.__name__
                )

            if request.data.get('new_function') is not None and not isinstance(request.data.get('new_function'), str):
                raise WrongTypeParameter(
                    fieldName="new_function",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_function').__class__.__name__
                )

            if request.data.get('new_status') is not None and not isinstance(request.data.get('new_status'), str):
                raise WrongTypeParameter(
                    fieldName="new_status",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_status').__class__.__name__
                )

            if request.data.get('new_linkedin') is not None and not isinstance(request.data.get('new_linkedin'), str):
                raise WrongTypeParameter(
                    fieldName="new_linkedin",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_linkedin').__class__.__name__
                )

            if request.data.get('new_photo') is not None and not isinstance(request.data.get('new_photo'), str):
                raise WrongTypeParameter(
                    fieldName="new_photo",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_photo').__class__.__name__
                )

            if request.data.get('new_description') is not None and not isinstance(request.data.get('new_description'), str):
                raise WrongTypeParameter(
                    fieldName="new_description",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_description').__class__.__name__
                )

            try:
                member_id = UUID(request.data.get('member_id'))
            except ValueError:
                raise EntityError('member_id')

            member = self.UpdateMemberUsecase(
                member_id=member_id,
                new_name=request.data.get('new_name'),
                new_function=request.data.get('new_function'),
                new_status=request.data.get('new_status'),
                new_linkedin=request.data.get('new_linkedin'),
                new_photo=request.data.get('new_photo'),
                new_description=request.data.get('new_description')
                )

            viewmodel = UpdateMemberViewmodel(member=member)

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