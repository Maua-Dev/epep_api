import json

from src.modules.update_member.app.update_member_presenter import lambda_handler, repo


def build_event(body: dict) -> dict:
    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/my/path",
        "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
        "cookies": [
            "cookie1",
            "cookie2"
        ],
        "headers": {
            "header1": "value1",
            "header2": "value1,value2"
        },
        "queryStringParameters": {
            "parameter1": "1"
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "<urlid>",
            "authentication": None,
            "authorizer": {
                "iam": {
                    "accessKey": "AKIA...",
                    "accountId": "111122223333",
                    "callerId": "AIDA...",
                    "cognitoIdentity": None,
                    "principalOrgId": None,
                    "userArn": "arn:aws:iam::111122223333:user/example-user",
                    "userId": "AIDA..."
                }
            },
            "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
            "domainPrefix": "<url-id>",
            "external_interfaces": {
                "method": "POST",
                "path": "/my/path",
                "protocol": "HTTP/1.1",
                "sourceIp": "123.123.123.123",
                "userAgent": "agent"
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "12/Mar/2020:19:03:58 +0000",
            "timeEpoch": 1583348638390
        },
        "body": json.dumps(body),
        "pathParameters": None,
        "isBase64Encoded": None,
        "stageVariables": None
    }


class Test_UpdateMemberPresenter:

    def test_update_member_name(self):
        member_id = str(repo.members[0].member_id)
        event = build_event({"member_id": member_id, "new_name": "Nome Atualizado"})

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"])['member_id'] == member_id
        assert json.loads(response["body"])['name'] == 'Nome Atualizado'

    def test_update_member_status(self):
        event = build_event({"member_id": str(repo.members[0].member_id), "new_status": "Desativado"})

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"])['status'] == 'Desativado'

    def test_update_member_all_fields(self):
        event = build_event({
            "member_id": str(repo.members[1].member_id),
            "new_name": "Todos Os Campos",
            "new_function": "Financeiro",
            "new_status": "Congelado",
            "new_linkedin": "https://www.linkedin.com/todos",
            "new_photo": "https://portalinterno.devmaua.com/assets/todos.webp",
            "new_description": "Descrição com todos os campos"
        })

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert body['name'] == 'Todos Os Campos'
        assert body['function'] == 'Financeiro'
        assert body['status'] == 'Congelado'
        assert body['linkedin'] == 'https://www.linkedin.com/todos'
        assert body['photo'] == 'https://portalinterno.devmaua.com/assets/todos.webp'
        assert body['description'] == 'Descrição com todos os campos'
        assert body['message'] == 'the member was updated successfully'
