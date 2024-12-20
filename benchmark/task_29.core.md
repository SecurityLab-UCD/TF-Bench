
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--truncate

# poly_type
Ad-hoc

# signature
```haskell
truncate :: (RealFrac a, Integral b) => a -> b
```   

# code
```haskell
truncate x =  fst (properFraction x)
```

# dependencies
## 0
```haskell
fst :: (a, b) -> a
```
## 1
```haskell
properFraction :: (RealFrac a, Integral b) => a -> (b, a)
```
