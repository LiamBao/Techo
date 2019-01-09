
# 链表成对交换
# 1->2->3->4转换成2->1->4->3.


# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

# class Solution:
#     # @param a ListNode
#     # @return a ListNode
#     def swapPairs(self, head):
#         if head != None and head.next != None:
#             next = head.next
#             head.next = self.swapPairs(next.next)
#             next.next = head
#             return next
#         return head

# s = Solution()
# l = ListNode([1,2,3,4,5,6,7,8])
# print(s.swapPairs())

# a = [1,2,3,7,9,1,5]
# b = [4,5,7,9,1,5]
# # 交叉链表求交点
# class Solution(object):
#     def get_first_node(self, l1, l2):
#         for i in range(1, min(len(l1), len(l2))):
#             if l1[-1] != l2[-1]:
#                 return None
#             else:
#                 if l1[-i] != l2[-i]:
#                     return l1[-i+1]

# print(Solution().get_first_node(a, b))


# # quick sort
# def quicksort(list):
#     if len(list) < 2:
#         return list
#     else:
#         mid = list[0]
#         lessthan = [i for i in list[1:] if i <= mid]
#         morethan = [i for i in list[1:] if i > mid]
#         finallist = quicksort(lessthan)+ [mid] + quicksort(morethan)
#     return finallist

# print(quicksort([2,4,6,7,1,2,43,33,3,323,1,5]))


# # 二叉树
# class Node(object):
#     def __init__(self, data, left=None, right=None):
#         self.data = data
#         self.left = left
#         self.right = right


# def lookup(root):
#     row = [root]
#     while row:
#         print(row)
#         row = [kid for item in row for kid in (item.left, item.right) if kid]
#     print(row)

# def deep(root):
#     if not root:
#         return
#     print(root.data)
#     deep(root.left)
#     deep(root.right)

# if __name__ == '__main__':
#     tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))
#     lookup(tree)
#     deep(tree)


# class Node(object):
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

# link = Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7, Node(8, Node(9)))))))))

# def rev(link):
#     pre = link
#     cur = link.next
#     pre.next = None
#     while cur:
#         tmp = cur.next
#         cur.next = pre
#         pre = cur
#         cur = tmp
#     return pre

# root = rev(link)
# while root:
#     print(root.data)
#     root = root.next

def MaxVal2(memo , w, v, index, last):  
    """ 
    得到最大价值 
    w为widght 
    v为value 
    index为索引 
    last为剩余重量 
    """  

    global numCount  
    numCount = numCount + 1  

    try:  
        #以往是否计算过分支，如果计算过，直接返回分支的结果  
        return memo[(index , last)]
    except:  
        #最底部  
        if index == 0:  
            #是否可以装入  
            if w[index] <= last:  
                return v[index]  
            else:  
                return 0  

        #寻找可以装入的分支  
        without_l = MaxVal2(memo , w, v, index - 1, last)  

        #如果当前的分支大于约束  
        #返回历史查找的最大值  
        if w[index] > last:  
            return without_l  
        else:  
            #当前分支加入背包，剪掉背包剩余重量，继续寻找  
            with_l = v[index] + MaxVal2(memo , w, v , index - 1, last - w[index])  

        #比较最大值  
        maxvalue = max(with_l , without_l)  
        #存储
        memo[(index , last)] = maxvalue  
        return maxvalue  

w = [0, 1, 4, 3, 1]   # 东西的重量 
v = [0, 1500, 3000, 2000, 2000]       # 东西的价值

numCount = 0  
memo = {} 
n = len(w) - 1
m = 4
print("{} caculate count :  {}".format(MaxVal2(memo , w, v, n, m) ,numCount))