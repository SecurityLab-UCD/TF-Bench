
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--map

# poly_type
Parametric

# signature
```haskell
map :: (a -> b) -> [a] -> [b]
```   

# code
```haskell
map _ []     = []
map f (x:xs) = f x : map f xs
```

# dependencies
