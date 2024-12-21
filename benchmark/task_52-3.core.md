
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--pure-Either

# poly_type
Parametric

# signature
```haskell
pure :: a -> Either e a
```   

# code
```haskell
pure = Right
```

# dependencies
## 0
```haskell
data Either a b = Left a | Right b
```
