
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--mod

# poly_type
Ad-hoc

# signature
```haskell
mod :: Integral a => a -> a -> a
```   

# code
```haskell
n `mod` d = snd (divMod n d)
```

# dependencies
## 0
```haskell
snd :: (a, b) -> b
```
## 1
```haskell
divMod :: Integral a => a -> a -> (a, a)
```
