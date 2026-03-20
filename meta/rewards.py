from meta.save_data import load_save, save_game


def reward_gems(amount):

    data = load_save()

    data["gems"] += amount

    save_game(data)