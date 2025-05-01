
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--(.)

# poly_type
Parametric

# signature
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```   

# code
```haskell
(.) f g = \x -> f (g x)
```

# dependencies
