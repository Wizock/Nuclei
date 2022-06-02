from typing import Any, Dict, Union

from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.recipe import session, thirdpartypasswordless
from supertokens_python.recipe.passwordless import (
    ContactEmailOrPhoneConfig,
    CreateAndSendCustomEmailParameters,
    CreateAndSendCustomTextMessageParameters,
)
from supertokens_python.recipe.thirdpartypasswordless import Apple, Github, Google


async def send_text_message(
    param: CreateAndSendCustomTextMessageParameters, user_context: Dict[str, Any]
):
    # send the SMS to this phone number.
    # it's in E.164 format (see https://www.twilio.com/docs/glossary/what-e164)
    phone_number = (param.phone_number,)
    print(phone_number)

    # this is the OTP string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "USER_INPUT_CODE"
    user_input_code: Union[str, None] = param.user_input_code
    print(user_input_code)

    # this is the magic link string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "MAGIC_LINK"
    url_with_link_code: Union[str, None] = param.url_with_link_code
    print(url_with_link_code)

    # This is the time in milliseconds for how long the url_with_link_code or user_input_code is valid for. */
    code_life_time = (param.code_life_time,)
    print(code_life_time)

    # pre_auth_session_id can be used for advanced customizations that need to
    # fetch data from the database or access something saved earlier in the process. */
    pre_auth_session_id: str = param.pre_auth_session_id
    print(pre_auth_session_id)

    # TODO: send SMS...
    return None  # See next step


async def send_email(
    param: CreateAndSendCustomEmailParameters, user_context: Dict[str, Any]
):
    # send the email to this email ID
    email = (param.email,)
    print(email)

    # this is the OTP string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "USER_INPUT_CODE"
    user_input_code: Union[str, None] = param.user_input_code
    print(user_input_code)

    # this is the magic link string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "MAGIC_LINK"
    url_with_link_code: Union[str, None] = param.url_with_link_code
    print(url_with_link_code)

    # This is the time in milliseconds for how long the url_with_link_code or user_input_code is valid for. */
    code_life_time = (param.code_life_time,)
    print(code_life_time)

    # pre_auth_session_id can be used for advanced customizations that need to
    # fetch data from the database or access something saved earlier in the process. */
    pre_auth_session_id: str = param.pre_auth_session_id
    print(pre_auth_session_id)

    # TODO: send email...
    return None


from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import thirdpartypasswordless, session
from typing import Any, Dict

from supertokens_python.recipe.passwordless import (
    ContactEmailOrPhoneConfig,
    CreateAndSendCustomEmailParameters,
    CreateAndSendCustomTextMessageParameters,
)

from supertokens_python.recipe.passwordless import (
    CreateAndSendCustomEmailParameters,
    CreateAndSendCustomTextMessageParameters,
)
from typing import Union, Dict, Any


async def send_text_message(
    param: CreateAndSendCustomTextMessageParameters, user_context: Dict[str, Any]
):
    # send the SMS to this phone number.
    # it's in E.164 format (see https://www.twilio.com/docs/glossary/what-e164)
    phone_number = (param.phone_number,)
    print(phone_number)

    # this is the OTP string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "USER_INPUT_CODE"
    user_input_code: Union[str, None] = param.user_input_code
    print(user_input_code)

    # this is the magic link string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "MAGIC_LINK"
    url_with_link_code: Union[str, None] = param.url_with_link_code
    print(url_with_link_code)

    # This is the time in milliseconds for how long the url_with_link_code or user_input_code is valid for. */
    code_life_time = (param.code_life_time,)
    print(code_life_time)

    # pre_auth_session_id can be used for advanced customizations that need to
    # fetch data from the database or access something saved earlier in the process. */
    pre_auth_session_id: str = param.pre_auth_session_id
    print(pre_auth_session_id)

    # TODO: send SMS...
    return None


async def send_email(
    param: CreateAndSendCustomEmailParameters, user_context: Dict[str, Any]
):
    # send the email to this email ID
    email = (param.email,)
    print(email)

    # this is the OTP string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "USER_INPUT_CODE"
    user_input_code: Union[str, None] = param.user_input_code
    print(user_input_code)

    # this is the magic link string. It will be defined if the flowType
    # is "USER_INPUT_CODE_AND_MAGIC_LINK" or "MAGIC_LINK"
    url_with_link_code: Union[str, None] = param.url_with_link_code
    print(url_with_link_code)

    # This is the time in milliseconds for how long the url_with_link_code or user_input_code is valid for. */
    code_life_time = (param.code_life_time,)
    print(code_life_time)

    # pre_auth_session_id can be used for advanced customizations that need to
    # fetch data from the database or access something saved earlier in the process. */
    pre_auth_session_id: str = param.pre_auth_session_id
    print(pre_auth_session_id)

    # TODO: send email...
    return None


init(
    app_info=InputAppInfo(
        app_name="Nuclei",
        api_domain="http://127.0.0.1:8080",
        website_domain="http://127.0.0.1:8080",
        api_base_path="/auth",
        website_base_path="/index",
    ),
    supertokens_config=SupertokensConfig(
        # These are the connection details of the app you created on supertokens.com
        connection_uri="https://1deec401e25411ecb140b5700135bf02-ap-southeast-1.aws.supertokens.io:3567",
        api_key="dtpl=I6jJRuO20ZctrY-DOUaCNkX3Q",
    ),
    framework="flask",
    recipe_list=[
        session.init(),  # initializes session features
        thirdpartypasswordless.init(
            flow_type="USER_INPUT_CODE_AND_MAGIC_LINK",
            contact_config=ContactEmailOrPhoneConfig(
                create_and_send_custom_text_message=send_text_message,
                create_and_send_custom_email=send_email,
            ),
            providers=[
                # We have provided you with development keys which you can use for testing.
                # IMPORTANT: Please replace them with your own OAuth keys for production use.
                Google(
                    client_id="1060725074195-kmeum4crr01uirfl2op9kd5acmi9jutn.apps.googleusercontent.com",
                    client_secret="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"
                    # ), Facebook(
                    #     client_id='FACEBOOK_CLIENT_ID',
                    #     client_secret='FACEBOOK_CLIENT_SECRET'
                ),
                Github(
                    client_id="467101b197249757c71f",
                    client_secret="e97051221f4b6426e8fe8d51486396703012f5bd",
                ),
                Apple(
                    client_id="4398792-io.supertokens.example.service",
                    client_key_id="7M48Y4RYDL",
                    client_private_key="-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgu8gXs+XYkqXD6Ala9Sf/iJXzhbwcoG5dMh1OonpdJUmgCgYIKoZIzj0DAQehRANCAASfrvlFbFCYqn3I2zeknYXLwtH30JuOKestDbSfZYxZNMqhF/OzdZFTV0zc5u5s3eN+oCWbnvl0hM+9IW0UlkdA\n-----END PRIVATE KEY-----",
                    client_team_id="YWQCXGJRJL",
                ),
            ],
        ),
    ],
)
