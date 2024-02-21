(
    (let a 1)
    (let b 1)
    (let temp 0)
    (let ret 0)
    (
        while ( > 4000000 b )
        (
            ( set temp b)
            ( set b ( + (a b)) )
            ( set a temp )
            ( if ( = 0 ( mod (b 2)) ) (
                set ret ( + ( b ret ))
                )
            )
            ( format b )
        )
    )
    (format ret)
)