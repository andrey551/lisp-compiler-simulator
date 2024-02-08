1. Give an array of number , which contain number and '(', ')'
each pair parentheses can hold multiple child, call x 
x also can seen as 1 node
build an tree that depend on value of each index on array
(integer represents for the number of child each node need to take)
ex1 : [1, 2, 1, 0, 2, 1, 0, 1, 0 ]
-> 
                1
                |
                2
               / \
              1   2
             /   / \ 
            0   1  1
                |  |
                0  0
ex2 : [1, 2, (1, 0, 2, 1, 0, 1, 1, 0), 1, 0]
->
                1
                |
                2
              /   \
            x       1
          /  \      |
        1     2     0
      /     /   \
    0      1     1
           |     |
           0     1
                 |
                 0    
-> Idea: using recursion(index):

assumn that item[index] have value x:
function exec(index):
  if(item[index] == '\('):
    item[index] = create_expression()
    while(item[index + 1] != '\)'):
      exec(index + 1)
      item[index].add_child(item[index + 1])
      item.pop(index + 1)
    item.pop(index + 1)
  elif(item[index] == '\)')
    pass
  else:
    for i in range(item[index]):
      execute(index + 1)
      item[index].add_child(item[index + 1])
      item.pop(index + 1)
---------------------------
