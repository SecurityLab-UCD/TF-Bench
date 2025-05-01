
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--div

# poly_type
Ad-hoc

# signature
```haskell
div :: Integral a => a -> a -> a
```   

# code
```haskell
n `div` d = fst (divMod n d)
```

# dependencies
## 0
```haskell
fst :: (a, b) -> a
```
## 1
```haskell
divMod :: Integral a => a -> a -> (a, a)
```
