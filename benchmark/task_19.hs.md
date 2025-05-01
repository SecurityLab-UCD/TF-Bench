
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--quot

# poly_type
Ad-hoc

# signature
```haskell
quot :: Integral => a -> a -> a
```   

# code
```haskell
n `quot` d = fst (quotRem n d)
```

# dependencies
## 0
```haskell
fst :: (a, b) -> a
```
## 1
```haskell
quotRem :: Integral => a -> a -> (a, a)
```
