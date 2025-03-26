def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input. Please provide the correct contact data."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner
