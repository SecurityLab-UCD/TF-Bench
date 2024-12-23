
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--negate

# poly_type
Ad-hoc

# signature
```haskell
negate :: Num a => a -> a
```   

# code
```haskell
negate x = 0 - x
```

# dependencies
## 0
```haskell
(-) :: Num a => a -> a -> a
```
