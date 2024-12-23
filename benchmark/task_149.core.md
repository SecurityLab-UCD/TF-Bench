
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--even

# poly_type
Ad-hoc

# signature
```haskell
even :: Integral a => a -> Bool
```   

# code
```haskell
even n = n `rem` 2 == 0
```

# dependencies
## 0
```haskell
rem :: Integral a => a -> a -> a
```
## 1
```haskell
(==) :: Eq a => a -> a -> Bool
```