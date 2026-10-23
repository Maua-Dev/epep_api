

#TODO faz um viewmodel que retorne isso - note que ele so vai usar o access_token, o refresh deve voltar nos headers:

# return {
#             "access_token": self.access_token,
#             "user": {
#                 "name": self.user_name,
#                 "role": self.user_role
#             },
#             "message": self.message
#         }