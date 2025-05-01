
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--repeat

# poly_type
Parametric

# signature
```haskell
repeat :: a -> [a]
```   

# code
```haskell
repeat x = xs where xs = x : xs
```

# dependencies
