
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--fmap-(,)

# poly_type
Parametric

# signature
```haskell
fmap :: (a0 -> b) -> (a, a0) -> (a, b)
```   

# code
```haskell
fmap f (x, y) = (x, f y)
```

# dependencies
