import itertools

def calculate_shapley_value(player, coalitions, value_function):
    marginal_contributions = []

    for coalition in coalitions:
        if player not in coalition:
            coalition_with_player = tuple(sorted(coalition + (player,)))
            value_with_player = value_function(coalition_with_player)
            value_without_player = value_function(coalition)
            marginal_contributions.append(value_with_player - value_without_player)

    return sum(marginal_contributions) / len(coalitions)

def shapley_value(participants, value_function):
    n = len(participants)
    players = list(participants.keys())
    coalitions = list(itertools.chain.from_iterable(itertools.combinations(players, r) for r in range(1, n + 1)))

    shapley_values = {}
    for player in players:
        shapley_values[player] = calculate_shapley_value(player, coalitions, value_function)

    return shapley_values

def fair_cost_distribution(participants, total_cost):
    shapley_values = shapley_value(participants, lambda coalition: sum(participants[player] for player in coalition))

    cost_distribution = {}
    for player in participants:
        cost_distribution[player] = total_cost * shapley_values[player] / sum(shapley_values.values())

    return cost_distribution

# Input: Number of users
num_users = int(input("Enter the number of users: "))

# Input: Distance traveled by each user
participants = {}
for i in range(1, num_users + 1):
    user_name = input(f"Enter the name of User{i}: ")
    distance = float(input(f"Enter the distance (in km) traveled by {user_name}: "))
    participants[user_name] = distance

# Input: Total fare
total_cost = float(input("Enter the total fare: "))

cost_distribution = fair_cost_distribution(participants, total_cost)

# Display the fair cost distribution
for player, cost_share in cost_distribution.items():
    print(f"{player}: {cost_share:.2f} INR")
