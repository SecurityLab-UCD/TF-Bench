
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--recip

# poly_type
Ad-hoc

# signature
```haskell
recip :: Fractional a => a -> a
```   

# code
```haskell
recip x =  one / x
```

# dependencies
## 0
```haskell
(/) :: Fractional a => a -> a -> a
```
## 1
```haskell
one :: Fractional a => a
```
