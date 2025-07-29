



from typing import Optional

from mcpcat.modules.internal import get_server_tracking_data, set_server_tracking_data
from mcpcat.modules.logging import write_to_log
from mcpcat.types import UserIdentity


def identify_session(server, request: any, context: any) -> None:
    """
    Identify the user based on the request and context.
    
    This function should be implemented by the user to provide custom identification logic.
    
    :param request: The request data containing user information.
    :param context: The context in which the request is made.
    :return: An instance of UserIdentity or None if identification fails.
    """
    data = get_server_tracking_data(server)

    if not data or not data.options or not data.options.identify:
        return
    
    if data.identified_sessions.get(data.session_id):
        write_to_log(f"User is already identified: {data.identified_sessions[data.session_id].userId}")
        return

    # Call the user-defined identify function
    try:
        identify_result = data.options.identify(request, context)
        if not identify_result or not isinstance(identify_result, UserIdentity):
            write_to_log(f"User identification function did not return a valid UserIdentity instance. Received: {identify_result}")
            return

        data.identified_sessions[data.session_id] = identify_result
        write_to_log(f"User identified: {identify_result.userId} - {identify_result.userName or 'Unknown Name'}")
        set_server_tracking_data(server, data)
    except Exception as e:
        write_to_log(f"Error occurred during user identification: {e}")
        return

    return identify_result
