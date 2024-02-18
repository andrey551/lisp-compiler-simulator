(
    (let a 1)
    (let b 1)
    (let temp 0)
    (let ret 0)
    (while ( < b 4000000 )
        (
            set temp b
            set b ( + (a b)) 
            set a temp 
            ( if ( = 0 ( mod (b 2))) (
                set ret ( + ( b ret ))
                )
            )
        )
    )
    (format ret)
)