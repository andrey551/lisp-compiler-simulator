1. Give an array of number , which contain number and '(', ')'
each pair parentheses can hold multiple child, call x 
x also can seen as 1 node
build an tree that depend on value of each index on array
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
    
    <!-- loop i -> x:
        if(item[index + i] == '\('):
            item[index + i] = create_expression()
            j = 0
            while(item[index + i + j] != '\)'):
                exec(index + i + j)
                item[index + i].add_child(item[index + i + j])
                item.delete(index + i + j)
                ++j
        
        if(item[index + i] == 0):
            item[index].add_child(item[index + i])
            item.delete(index + i)
        else :
            exec(index +i)
            item[index].add_child(item[index + i])
            item.delete(index + i) -->

