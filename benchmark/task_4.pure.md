
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Tuple.hs--curry

# poly_type
Parametric

# signature
```haskell
g :: ((a, b) -> c) -> a -> b -> c
```   

# code
```haskell
g f x y             =  f (x, y)
```

# dependencies
