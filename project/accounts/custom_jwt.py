# import logging
# import logging

# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.authentication import JWTAuthentication

# logger = logging.getLogger(__name__)
# logger = logging.getLogger(__name__)

# class CustomJWTAuthentication(JWTAuthentication):
# class CustomJWTAuthentication(JWTAuthentication):

#     # def authenticate(self, request):
#     #     logger.info("Authenticating request...")
#     #     raw_token = self.get_raw_token(self.get_header(request))
#     #     if raw_token is None:
#     #         logger.warning("No token found in request")
#     #         return None

#     #     validated_token = self.get_validated_token(raw_token)
#     #     if not validated_token:
#     #         logger.error("Invalid token")
#     #         return None

#     #     logger.info("Token is valid")
#     #     return self.get_user(validated_token), validated_token
#     def authenticate(self, request):
#             header = self.get_header(request)
#             logger.info("header : ")
#             logger.info( header)

#             if header is None:
#                 logger.info( " header is None:")
#                 return None

#             raw_token = self.get_raw_token(header)
#             logger.info("raw_token")
#             logger.info(raw_token)

#             if raw_token is None:
#                 logger.info("raw_token is None")
#                 return None

#             validated_token = self.get_validated_token(raw_token)
#             logger.info("validated_token")
#             logger.info(validated_token)
#             logger.info("self.get_user(validated_token)")
#             logger.info(self.get_user(validated_token))

#             return self.get_user(validated_token), validated_token
