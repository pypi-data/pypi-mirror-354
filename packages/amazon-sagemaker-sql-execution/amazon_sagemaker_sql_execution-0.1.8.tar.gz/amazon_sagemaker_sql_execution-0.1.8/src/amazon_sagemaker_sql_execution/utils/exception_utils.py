def handle_endpoint_connection_error(error):
    """Handles Boto EndpointConnectionError."""
    # TODO: exact error message to be updated after PM sign off.
    raise ConnectionError(
        "{}. Please check your network settings or contact support for assistance.".format(
            str(error)
        )
    )
