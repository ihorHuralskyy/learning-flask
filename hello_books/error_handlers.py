def validation_error(error):
    return {"error": error.messages, "valid_data": error.valid_data}, 422


def general_exception(error):
    return {"error": repr(error)}, 500


def entity_404(error):
    return {"error": error.description}, 404
