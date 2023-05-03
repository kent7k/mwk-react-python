from rest_framework import serializers


class ErrorMessagesSerializersMixin:
    """
    A mixin for serializers that makes it easy to raise exceptions from `default_error_messages`.

    This mixin provides a helper method `fail()` that raises a validation error with the
    specified error message key from the `error_messages` dictionary.

    This mixin was created because the default `self.fail()` method of serializers
    does not support errors in the form of dictionaries.
    """

    error_messages = {}

    def fail(self, key):
        """
        Raises a validation error with the specified error message key from the `error_messages` dictionary.

        If the key is not found in the dictionary, a `KeyError` is raised with a
        custom error message indicating the class name and the missing key.
        """

        try:
            msg = self.error_messages[key]
        except KeyError:
            class_name = type(self).__name__
            error_message = f"ValidationError raised by `{class_name}`, but error key `{key}` does not exist in the `error_messages` dictionary."
            raise KeyError(error_message)

        raise serializers.ValidationError(msg, code=key)
