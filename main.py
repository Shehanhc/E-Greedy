import random

steps = 10000000
number_of_arms = 5
cumulative_reward = 0
arm_means = {}
arm_estimates = {}
arm_selection_count = {}
explore_count = 0
exploit_count = 0
highest_mean = -2


# Function to get the arm with the highest estimate
def get_highest_estimated_arm():
    current_highest_value = 0
    current_highest_arm = 0

    # Loop through the arms to check
    for key in arm_estimates:
        # Set the first values from the first one and compare against it
        if key == 1:
            current_highest_arm = key
            current_highest_value = arm_estimates[key]
        else:
            if arm_estimates[key] > current_highest_value:
                current_highest_value = arm_estimates[key]
                current_highest_arm = key

    return current_highest_arm


# Function to update the estimate of the selected arm and update the cumulative reward
def update_estimate_and_reward(arm, current_cumulative_reward):
    # Get the current reward using the mean for the selected arm and a standard deviation of 1
    current_reward = random.gauss(arm_means[arm], 1)

    # Get the arm's current estimate
    current_estimate = arm_estimates[arm]

    # Get the number of times the current arm was selected
    current_selection_number = arm_selection_count[arm] + 1

    # Calculate the new estimate
    new_estimate = current_estimate + ((current_reward - current_estimate) / current_selection_number)

    # Update the cumulative reward
    current_cumulative_reward += current_reward

    # Update the estimate and the selection count for this arm
    arm_estimates.update({arm: new_estimate})
    arm_selection_count.update({arm: current_selection_number})

    return current_cumulative_reward


# Loop through the arms to initialize
for arm in range(number_of_arms):
    # Generate a random mean between -1 and 3
    # arm_mean = round(random.uniform(-1, 3), 2)
    arm_mean = (arm+1)*(arm+1)

    # Set the newly generated mean for the arm
    arm_means.update({arm+1: arm_mean})

    # Set the estimate to each arm as 0
    arm_estimates.update({arm+1: 0})

    # Set the selection count for each arm as 0
    arm_selection_count.update({arm+1: 0})

    # Check which mean is the highest and keep track of it
    if arm_mean > highest_mean:
        highest_mean = arm_mean

    print("Setting mean of arm " + str(arm+1) + " to " + str(arm_mean))
print()


# Loop through the given number of steps
for step in range(steps):
    # Generate a number between 0 an 1 to 1 decimal point.
    step_probability = round(random.uniform(0,1), 1)

    # Explore with probability 0.1
    if step_probability < 0.2:  # Explore
        # Pick a random arm
        arm = random.randrange(1, number_of_arms + 1)

        # Call the update_estimate_and_reward method
        cumulative_reward = update_estimate_and_reward(arm, cumulative_reward)

        # Update the count for number of times explored
        explore_count += 1
    else:  # Exploit
        # Get the arm with the highest estimate
        highest_arm = get_highest_estimated_arm()

        # Call the update_estimate_and_reward method
        cumulative_reward = update_estimate_and_reward(highest_arm, cumulative_reward)

        # Update the count for number of times exploited
        exploit_count += 1


# Print results
print("Explored " + str(explore_count) + " times")
print("Exploited " + str(exploit_count) + " times")
print()

print("Total Reward: " + str(round(cumulative_reward, 2)))
print("Possible Max reward: " + str(round(highest_mean*steps, 2)))

regret = (highest_mean*steps)-cumulative_reward
print("Total Regret: " + str(round(regret, 2)))
print("Regret: " + str(regret/steps))
print()

for arm in range(number_of_arms):
    print("Arm " + str(arm+1) + " was selected " + str(arm_selection_count[arm+1]) + " times")

print()

for arm in range(number_of_arms):
    print("Arm " + str(arm+1) + " estimate " + str(arm_estimates[arm+1]))