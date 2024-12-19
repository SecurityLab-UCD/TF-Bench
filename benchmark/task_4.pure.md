
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Tuple.hs--curry

# poly_type
Parametric

# signature
```haskell
f1 :: ((a, b) -> c) -> a -> b -> c
```   

# code
```haskell
f1 f x y             =  f (x, y)
```

# dependencies
