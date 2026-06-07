import random
class utils:
    #create a stack containing areas of different weights and randomly choose one
    @staticmethod
    def probability_stack(data):
        total_weight=0
        for stack in data:
            total_weight+=stack[0]
        picked_number=random.uniform(0,total_weight)
        cumulative_weight=0
        for stack in data:
            if picked_number>= cumulative_weight and picked_number<(cumulative_weight+stack[0]):
                return stack[1]
            cumulative_weight+=stack[0]
        return data[0][1]