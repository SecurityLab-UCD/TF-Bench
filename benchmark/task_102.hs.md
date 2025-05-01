
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--zip

# poly_type
Parametric

# signature
```haskell
zip :: [a] -> [b] -> [(a,b)]
```   

# code
```haskell
zip (a:as) (b:bs) = (a,b) : zip as bs
zip []     _bs    = []
zip _as    []     = []
```

# dependencies
