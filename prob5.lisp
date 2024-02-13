( defun gcd (g h) (
    ( if ( = g 0 ) 
        ( return h )
        ( return ( call gcd ( h mod ( g h ))))
    )
)

( defun least_common_multiple (a b) (
    return ( / (( * ( a b) ) (call gcd ( a b)))) )
)

(let res 1)
(let i 1)
(
    while ( < i 21 )
    (
        set res (call smallest_divisor ( res i))
        set i ( + ( i 1) )  
    )
)                   
(format t res))