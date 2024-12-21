
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--pure-(,)

# poly_type
Parametric

# signature
```haskell
pure :: a0 -> (a, a0)
```   

# code
```haskell
pure x = (mempty, x)
```

# dependencies
## 0
```haskell
mempty :: a
```
