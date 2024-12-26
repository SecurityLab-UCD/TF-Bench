
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--filter

# poly_type
Parametric

# signature
```haskell
filter :: (a -> Bool) -> [a] -> [a]
```   

# code
```haskell
filter f []    = []
filter f (x:xs)
  | f x        = x : filter f xs
  | otherwise  = filter f xs
```

# dependencies
