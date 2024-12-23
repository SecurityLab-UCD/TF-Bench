
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--fmap-Either

# poly_type
Parametric

# signature
```haskell
fmap :: (a0 -> b) -> Either a a0 -> Either a b
```   

# code
```haskell
fmap _ (Left x) = Left x
fmap f (Right y) = Right (f y)
```

# dependencies
## 0
```haskell
data Either a b = Left a | Right b
```
