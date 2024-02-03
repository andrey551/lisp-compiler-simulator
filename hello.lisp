(format t "hello world")
(setq x 5)
(loop          
  :for i :from 1 :to x 
  :do (print (* i i)))