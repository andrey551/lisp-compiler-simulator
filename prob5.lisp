((defun gcd (a, b) (
    if( b = 0) 
    (return a) 
    ( return (call (gcd (b, mod (a, b)))))
))

(defun least_common_multiple (a, b) (
    return ( / (* (a, b) , (call gcd (a, b))))
))

(let res = 1)
(
    loop
    :for i :from 2 :to 20
    (
        set res (call smallest_divisor (res, i))  
    )
)
(format t res))