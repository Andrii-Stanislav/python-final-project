def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError:
            return "Contact not found."
        except IndexError as ie:
            return str(ie)
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner
