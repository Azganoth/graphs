

true_false_br_abbr = {
    's': True,  # Sim
    'n': False,  # Não
}


def ask_true_false_br(message: str) -> bool:
    """Asks the user for a true or false response. Repeating
    the question till **s** or **n** is given as response.

    Args:
        message: The message to be shown to the user.

    Returns:
        The user response.
    """
    while (response := input(message).strip().lower()) not in true_false_br_abbr.keys():
        pass
    return true_false_br_abbr[response]
