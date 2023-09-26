def save_money_for_workout(user):
    savings_per_workout = 50  # A fixed amount for each workout

    # Ensure the user has enough in their bank account
    if user.bank_balance < savings_per_workout:
        return False

    # Transfer the savings from the bank account to the savings account
    user.bank_balance -= savings_per_workout
    user.savings_balance += savings_per_workout

    return user.savings_balance