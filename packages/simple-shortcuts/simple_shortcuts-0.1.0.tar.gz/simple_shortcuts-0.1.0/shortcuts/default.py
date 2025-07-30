# default constant for differentiating between unset function params and null values.
# ie:
#     def request(timeout=DEFAULT):
#         if timeout is DEFAULT:
#             ...
#         elif timeout is None:
#             ...
DEFAULT = object()
