
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--flip

# poly_type
Parametric

# signature
```haskell
flip :: (a -> b -> c) -> b -> a -> c
```   

# code
```haskell
flip f x y =  f y x
```

# dependencies
