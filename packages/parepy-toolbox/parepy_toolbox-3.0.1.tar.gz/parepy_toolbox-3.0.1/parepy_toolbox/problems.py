# def structural_problems(type: str, name: str):

#     if type == 'sampling':
#         if name == 'book - Chang - page 558':
#             def obj_(x):
#                 g_0 = 12.5 * x[0] ** 3 - x[1]
#                 return [g_0]
#             obj = obj_
#             d = {'type': 'normal', 'parameters': {'mean': 1., 'std': 0.1}}
#             l = {'type': 'normal', 'parameters': {'mean': 10., 'std': 1.}}
#             var = [d, l]
#     else:
#         if name == 'book - Chang - page 558':
#             def obj_(x):
#                 g_0 = 12.5 * x[0] ** 3 - x[1]
#                 return g_0
#             obj = obj_
#             d = {'type': 'normal', 'parameters': {'mean': 1., 'std': 0.1}}
#             l = {'type': 'normal', 'parameters': {'mean': 10., 'std': 1.}}
#             var = [d, l]

#     return obj, var
