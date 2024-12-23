
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--logBase

# poly_type
Ad-hoc

# signature
```haskell
logBase :: Floating a => a -> a -> a
```   

# code
```haskell
logBase x y = log y / log x
```

# dependencies
## 0
```haskell
log :: Floating a => a -> a
```
## 1
```haskell
(/) :: Fractional a => a -> a -> a
```
