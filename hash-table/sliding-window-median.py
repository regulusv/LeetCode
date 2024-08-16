class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        def get_median():
            if k % 2 == 0:
                return (-lo[0] + hi[0]) / 2.0
            else:
                return -lo[0]

        lo, hi = [], []  # 最大堆和最小堆 (用负数表示最大堆)
        hash_table = defaultdict(int)  # 延迟删除的哈希表
        medians = []

        for i in range(k):
            heapq.heappush(lo, -nums[i])
        for _ in range(k // 2):
            heapq.heappush(hi, -heapq.heappop(lo))

        for i in range(k, len(nums) + 1):
            medians.append(get_median())

            if i == len(nums):
                break

            out_num = nums[i - k]  # 即将移出窗口的元素
            in_num = nums[i]  # 新进入窗口的元素
            balance = 0

            # 处理窗口中移出的元素
            # -lo[0] is smallest of the heap, 
            # lo[0] has the largest  numeric "value"
            if out_num <= -lo[0]: 
                balance -= 1
            else:
                balance += 1
            hash_table[out_num] += 1

            # 处理新进入窗口的元素
            if in_num <= -lo[0]:
                balance += 1
                heapq.heappush(lo, -in_num)
            else:
                balance -= 1
                heapq.heappush(hi, in_num)

            # 平衡堆
            if balance < 0:  # lo需要更多有效元素
                heapq.heappush(lo, -heapq.heappop(hi))
                balance += 1
            if balance > 0:  # hi需要更多有效元素
                heapq.heappush(hi, -heapq.heappop(lo))
                balance -= 1

            # 延迟删除无效元素
            while lo and hash_table[-lo[0]] > 0:
                hash_table[-lo[0]] -= 1
                heapq.heappop(lo)
            while hi and hash_table[hi[0]] > 0:
                hash_table[hi[0]] -= 1
                heapq.heappop(hi)

        return medians