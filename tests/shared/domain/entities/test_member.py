import pytest
import uuid

from src.shared.domain.entities.member import Member
from src.shared.domain.enums.member_function_enum import MemberFunctionEnum
from src.shared.helpers.errors.domain_errors import EntityError


class Test_Member:

    def test_member(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
            description="Exemplo de descrição do membro"
        )
        assert isinstance(member.member_id, uuid.UUID)
        assert member.name == "Nome Completo do Membro"
        assert member.member_function == "Marketing"
        assert str(member.linkedin) == "https://www.linkedin.com/"
        assert str(member.member_photo) == "https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png"
        assert member.description == "Exemplo de descrição do membro"



    # model_config

    def test_member_extra_field(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro",
                extra_field="Campo extra"
            )



    # name

    def test_member_name_with_numbers(self):
        with pytest.raises(EntityError):
            member = Member(
                name="N0me 1nválido",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_name_with_invalid_symbols(self):
        with pytest.raises(EntityError):
            member = Member(
                name="[Nome Inválido!]",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_name_too_short(self):
        with pytest.raises(EntityError):
            member = Member(
                name="N",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_name_min_length(self):
        member = Member(
            name="Ju",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
            description="Exemplo de descrição do membro"
        )
        assert member.name == "Ju"


    def test_member_name_empty(self):
        with pytest.raises(EntityError):
            member = Member(
                name="",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_has_no_name(self):
        with pytest.raises(EntityError):
            member = Member(
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )



    # member_function

    def test_member_function_invalid(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Cargo Inválido",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_function_redacao_enum(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function=MemberFunctionEnum.REDACAO,
            linkedin="https://www.linkedin.com/",
            member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
            description="Exemplo de descrição do membro"
        )
        assert member.member_function == "Redacao"


    def test_member_function_marketing_enum(self):
            member = Member(
                name="Nome Completo do Membro",
                member_function=MemberFunctionEnum.MARKETING,
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )
            assert member.member_function == "Marketing"


    def test_member_function_empty(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_has_no_function(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )



    # linkedin

    def test_member_linkedin_invalid_url(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="Não é uma url",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_linkedin_no_scheme(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="www.linkedin.com",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_linkedin_empty(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_linkedin_normalizes_slash(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com",
            member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
            description="Exemplo de descrição do membro"
        )
        assert str(member.linkedin) == "https://www.linkedin.com/"


    def test_member_has_no_linkedin(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )



    # member_photo

    def test_member_photo_invalid_url(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="Não é URL",
                description="Exemplo de descrição do membro"
            )


    def test_member_photo_no_scheme(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Exemplo de descrição do membro"
            )


    def test_member_photo_url_no_file_extension(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/",
                description="Exemplo de descrição do membro"
            )


    def test_member_photo_accepts_png(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://www.exemplo.com/imagem.png",
            description="Exemplo de descrição do membro"
        )
        assert str(member.member_photo).endswith(".png")


    def test_member_photo_accepts_jpg(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://www.exemplo.com/imagem.jpg",
            description="Exemplo de descrição do membro"
        )
        assert str(member.member_photo).endswith(".jpg")


    def test_member_photo_accepts_jpeg(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://www.exemplo.com/imagem.jpeg",
            description="Exemplo de descrição do membro"
        )
        assert str(member.member_photo).endswith(".jpeg")


    def test_member_photo_accepts_webp(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://www.exemplo.com/imagem.webp",
            description="Exemplo de descrição do membro"
        )
        assert str(member.member_photo).endswith(".webp")


    def test_member_photo_rejects_other_extensions(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://www.exemplo.com/imagem.pdf",
                description="Exemplo de descrição do membro"
            )


    def test_member_photo_case_insensitive(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://www.exemplo.com/imagem.PNG",
            description="Exemplo de descrição do membro"
        )
        assert str(member.member_photo).endswith(".PNG")


    def test_member_photo_empty(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="",
                description="Exemplo de descrição do membro"
            )


    def test_member_has_no_photo(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                description="Exemplo de descrição do membro"
            )



    # description

    def test_member_description_with_numbers(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
            description="Descrição: membro melhorou em 10%. (com parênteses)!"
        )
        assert member.description == "Descrição: membro melhorou em 10%. (com parênteses)!"


    def test_member_description_too_short(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description="Abcd"
            )


    def test_member_description_min_length(self):
        member = Member(
            name="Nome Completo do Membro",
            member_function="Marketing",
            linkedin="https://www.linkedin.com/",
            member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
            description="Curto"
        )
        assert member.description == "Curto"


    def test_member_description_empty(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png",
                description=""
            )


    def test_member_has_no_description(self):
        with pytest.raises(EntityError):
            member = Member(
                name="Nome Completo do Membro",
                member_function="Marketing",
                linkedin="https://www.linkedin.com/",
                member_photo="https://portalinterno.devmaua.com/assets/logo_dev-ec58e665.png"
            )
