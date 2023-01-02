import pprint
import random

res = []
interests_list = [str(i) for i in range(2, 72)]
for i in range(1, 100):
    res.append(
        f"UPDATE profiles SET interests = '{{{','.join(random.choice(interests_list) for j in range(random.randint(2, 6)))}}}' WHERE user_id = {i};"
    )
print(" ".join(res))
