
def is_good(mid, nums, k):
    volumes = 1
    current_sum = 0
    for pages in nums:
        if current_sum + pages > mid:
            volumes += 1
            current_sum = pages
            if volumes > k:
                return False
        else:
            current_sum += pages
    return True

def solve():
    n = int(input())
    nums = list(map(int, input().split()))
    k = int(input())
    
    left = max(nums)
    right = sum(nums)
    while left<right:
        mid = (left+ right) //2
        if is_good(mid, nums, k): right = mid
        else: left = mid+1
    print(right)

    
if __name__ == "__main__":
    solve()