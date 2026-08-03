import random
import os

def round_to_step(value):
        step = 25
        return round(value / step) * step
 
def init_variables():
    while True: 
        try:
            n = int(input("How many numbers will be in game: "))
            if n > 0: break
        except:
            print("Please enter an integer number.")
    
    while True:
        try:
            lower = int(input("Enter lower limit: "))
            if lower > 0: break
        except:
            print("Please enter an integer number.")
    
    while True:
        try:
            upper = int(input("Enter upper limit: "))
            if upper > lower: break
        except:
            print("Upper less than lower. Try again.")
    
    while True:
        try:
            
            different = int(input("Enter different in percent: "))
            if different >=0 and different <= 100:
                different = round_to_step(different) /100
                break
            else:
                print("Invalid number! Try again.")
        except ValueError:
            print("Please enter an integer number.")
    
    return n, lower, upper, different

def init_list_dp(n, lower, upper):
    nums = []
    for i in range(n):
        t = random.randint(lower, upper)
        nums.append(t)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = nums[i]
    return nums, dp

def update_dp(nums, n):
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = nums[i]
    return dp

def maybe_change(value, p, new_value):
        return random.choices([value, new_value], weights=[1-p, p])[0]

def rand_to_delete(nums, n, different, correct_ans, another_ans, sum_comp):
    correct_ans = maybe_change(correct_ans, different, another_ans)
    sum_comp += nums[correct_ans]
    nums.pop(correct_ans)
    n -=1
    return nums, n, sum_comp

def choice_comp(nums, dp, n, different, sum_comp):
    if n == 1:
        sum_comp += nums[0]
        nums.pop()
        n = 0
        print("Comp made move.")
        return nums, n, sum_comp
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            left = nums[i] - dp[i + 1][j]
            right = nums[j] - dp[i][j - 1]
            dp[i][j] = max(left, right)
            
    if left > right:
        correct_ans = -1
        another_ans = 0
        nums, n, sum_comp = rand_to_delete(nums, n, different, correct_ans, another_ans, sum_comp)
    else:
        correct_ans = 0
        another_ans = -1
        nums, n, sum_comp = rand_to_delete(nums, n, different, correct_ans, another_ans, sum_comp)
    print("Comp made move.")
    return nums, n, sum_comp

def choice_player(nums, n, sum_player):
    while True:
        try:
            number = int(input(f"Choice number to grab from:\n{nums}\nEnter 1(left) or 2(right) number: "))
            if number == 1:
                sum_player += nums[0]
                nums.pop(0)
                break
            elif number == 2:
                sum_player += nums[-1]
                nums.pop()
                break
        except ValueError:
            print("Please enter an integer number.")
    n -= 1
    return nums, n, sum_player
    
def play_game():
    n, lower, upper, different = init_variables()
    nums, dp = init_list_dp(n, lower, upper)
    sum_player = 0
    sum_comp = 0
    while nums:
        nums, n, sum_player = choice_player(nums, n, sum_player)
        if not nums:
            break
        dp = update_dp(nums, n)
        nums, n, sum_comp = choice_comp(nums, dp, n, different, sum_comp)
    
    dist = abs(sum_comp - sum_player)
    if sum_player > sum_comp:
        print(f"You win on {dist} point. Congratulations!!!")
    elif sum_player < sum_comp:
        print(f"You lose on {dist} point. Try again.")
    else:
        print("Draw. Your game was like me in 7 y.e")
    os.system("pause")


if __name__ == "__main__":
    play_game() 

#