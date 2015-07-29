lastButOne xs
    | len <= 1  = error "list too short"
    | otherwise = head (drop (len - 2) xs)
    where len = length xs
